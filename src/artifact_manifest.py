"""Create deterministic hashes for final project artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from src.config import ROOT


def sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_artifact_manifest() -> dict[str, Any]:
    """Hash canonical deliverables while excluding transient deployment output."""

    patterns = [
        "data/raw/Live_20210128.csv",
        "data/processed/*.csv",
        "data/generated/*.csv",
        "notebooks/*.ipynb",
        "outputs/analysis_summary.json",
        "outputs/tables/*.csv",
        "outputs/exercise_summaries/*.txt",
        "visualizations/static/*.png",
        "visualizations/interactive/*.html",
        "report/report.*",
    ]
    paths = sorted(
        {path for pattern in patterns for path in ROOT.glob(pattern) if path.is_file()},
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    manifest = {
        "schema_version": 1,
        "algorithm": "sha256",
        "artifact_count": len(paths),
        "artifacts": {
            path.relative_to(ROOT).as_posix(): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in paths
        },
    }
    destination = ROOT / "outputs" / "artifact_manifest.json"
    destination.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest
