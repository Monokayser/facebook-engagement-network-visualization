"""Cross-surface contracts for notebooks, reports, and generated websites."""

from __future__ import annotations

import json
import re
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import nbformat

ROOT = Path(__file__).resolve().parents[1]


class _ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        del tag
        self.references.extend(
            value
            for name, value in attrs
            if name in {"href", "src"} and value is not None
        )


def test_canonical_summary_and_manifests_have_supported_schema() -> None:
    summary = json.loads(
        (ROOT / "outputs" / "analysis_summary.json").read_text(encoding="utf-8")
    )
    artifacts = json.loads(
        (ROOT / "outputs" / "artifact_manifest.json").read_text(encoding="utf-8")
    )
    site = json.loads(
        (ROOT / "website" / "site_manifest.json").read_text(encoding="utf-8")
    )
    assert summary["runtime"]["seed"] == 42
    assert artifacts["schema_version"] == 1
    assert artifacts["artifact_count"] == len(artifacts["artifacts"])
    assert site["schema_version"] == 1
    assert len(site["exercise_pages"]) == 7


def test_all_notebooks_are_executed_without_error_outputs() -> None:
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
        assert code_cells, path.name
        assert all(cell.execution_count is not None for cell in code_cells), path.name
        assert not any(
            output.output_type == "error"
            for cell in code_cells
            for output in cell.get("outputs", [])
        ), path.name


def test_every_exercise_page_contains_required_evidence() -> None:
    pages = sorted((ROOT / "website" / "exercises").glob("[0-9][0-9]-*.html"))
    assert len(pages) == 7
    for path in pages:
        text = path.read_text(encoding="utf-8")
        for required in (
            "Exercise ",
            "All seven exercises",
            "Objective and data source",
            "Verified result and visualization",
            "Python implementation",
            "Interpretation and limitation",
            "Download exercise data",
            "blob/main/src/",
            "<pre><code>",
        ):
            assert required in text, (path.name, required)


def test_exercise_index_is_an_ordered_seven_step_pathway() -> None:
    text = (ROOT / "website" / "exercises" / "index.html").read_text(encoding="utf-8")
    assert 'class="exercise-roadmap"' in text
    assert text.count('class="exercise-card"') == 7
    positions = [
        text.index(f'class="exercise-number">{number:02d}') for number in range(1, 8)
    ]
    assert positions == sorted(positions)


def test_exercise_pages_have_sequential_navigation() -> None:
    pages = sorted((ROOT / "website" / "exercises").glob("[0-9][0-9]-*.html"))
    first = pages[0].read_text(encoding="utf-8")
    last = pages[-1].read_text(encoding="utf-8")
    assert "Exercise 02 &rarr;" in first
    assert "&larr; Exercise 06" in last
    for number, page in enumerate(pages, start=1):
        text = page.read_text(encoding="utf-8")
        assert f"Exercise {number} of 7" in text


def test_static_site_uses_relative_internal_paths() -> None:
    for path in (ROOT / "website").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        assert "file:///" not in text
        assert str(ROOT) not in text
        internal = re.findall(r'(?:href|src)="([^"]+)"', text)
        assert not any(value.startswith("/") for value in internal), path


def test_every_static_site_link_and_embed_resolves() -> None:
    missing: list[tuple[str, str]] = []
    for page in (ROOT / "website").rglob("*.html"):
        parser = _ReferenceParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for value in parser.references:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                missing.append((page.relative_to(ROOT).as_posix(), value))
    assert not missing


def test_report_copies_are_byte_identical() -> None:
    for name in ("report.md", "report.docx", "report.pdf"):
        copies = [
            ROOT / "report" / name,
            ROOT / "public" / name,
            ROOT / "website" / "report" / name,
        ]
        hashes = {sha256(path.read_bytes()).hexdigest() for path in copies}
        assert len(hashes) == 1, name


def test_no_stale_domain_metric_claim_remains() -> None:
    tracked_text = [
        ROOT / "README.md",
        ROOT / "exercises" / "README.md",
        ROOT / "report" / "report.md",
        ROOT / "app" / "page.tsx",
    ]
    for path in tracked_text:
        assert "0.3663" not in path.read_text(encoding="utf-8")


def test_publication_targets_github_pages_only() -> None:
    assert not (ROOT / ".openai" / "hosting.json").exists()
    public_text = [
        ROOT / "README.md",
        ROOT / "report" / "report.md",
        ROOT / "src" / "report_generator.py",
        ROOT / "src" / "site_generator.py",
        ROOT / "website" / "index.html",
    ]
    forbidden = ("chatgpt.site", "circleofexpose", "secondary deployment")
    for path in public_text:
        text = path.read_text(encoding="utf-8").lower()
        assert not any(value in text for value in forbidden), path
