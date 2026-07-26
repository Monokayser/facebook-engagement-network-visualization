"""Generate the GitHub Pages site and shared static exercise pages."""

from __future__ import annotations

import html
import inspect
import json
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

from src import graph_generators, network_analysis, visualization
from src.config import (
    ANALYSIS_SUMMARY,
    INTERACTIVE,
    PROCESSED_CSV,
    PUBLIC,
    ROOT,
    STATIC,
    STUDENT,
    WEBSITE,
)

REPOSITORY_URL = (
    "https://github.com/Monokayser/facebook-engagement-network-visualization"
)
PAGES_URL = "https://monokayser.github.io/facebook-engagement-network-visualization/"

EXERCISES = [
    {
        "number": 1,
        "slug": "weighted-adjacency",
        "title": "Weighted adjacency representations",
        "source": "Supplied Section 8.2 G_transport graph",
        "dataset": "outputs/tables/g_transport_adjacency_matrix.csv",
        "kind": "Graph representation",
        "deliverable": "Adjacency list and 7 x 7 weighted matrix",
        "source_paths": [
            "src/graph_generators.py",
            "src/network_analysis.py",
        ],
        "functions": [
            graph_generators.build_transport_graph,
            network_analysis.transport_representations,
        ],
        "image": None,
        "interactive": None,
    },
    {
        "number": 2,
        "slug": "six-layout-comparison",
        "title": "Six-layout comparison",
        "source": "Supplied Section 8.3 G_ppi graph",
        "dataset": "outputs/analysis_summary.json",
        "kind": "Layout comparison",
        "deliverable": "Six layouts and a combined comparison figure",
        "source_paths": [
            "src/graph_generators.py",
            "src/visualization.py",
        ],
        "functions": [
            graph_generators.build_ppi_graph,
            visualization.create_layout_figures,
        ],
        "image": "g_ppi_layout_comparison.png",
        "interactive": None,
    },
    {
        "number": 3,
        "slug": "student-course-bipartite",
        "title": "Student-course bipartite network",
        "source": "Stored synthetic student, course, and enrollment CSV files",
        "dataset": "data/generated/enrollments.csv",
        "kind": "Bipartite network",
        "deliverable": "CSV-backed enrollment graph and degree findings",
        "source_paths": [
            "src/graph_generators.py",
            "src/network_analysis.py",
            "src/visualization.py",
        ],
        "functions": [
            graph_generators.load_student_course_graph,
            network_analysis.student_course_findings,
        ],
        "image": "student_course_bipartite_graph.png",
        "interactive": None,
    },
    {
        "number": 4,
        "slug": "weighted-barabasi-albert",
        "title": "Weighted Barabasi-Albert graph",
        "source": "Supplied Section 6 Barabasi-Albert graph definition",
        "dataset": "outputs/tables/barabasi_albert_edge_weights.csv",
        "kind": "Weighted network",
        "deliverable": "Weighted graph, baseline graph, and edge table",
        "source_paths": [
            "src/graph_generators.py",
            "src/visualization.py",
        ],
        "functions": [
            graph_generators.add_reproducible_edge_weights,
            visualization.create_weighted_ba_figures,
        ],
        "image": "barabasi_albert_weighted.png",
        "interactive": None,
    },
    {
        "number": 5,
        "slug": "generative-model-comparison",
        "title": "Generative-model comparison",
        "source": "Supplied Section 3 graph-model definitions",
        "dataset": "outputs/tables/generative_models_comparison.csv",
        "kind": "Model comparison",
        "deliverable": "Metric table and degree-distribution figures",
        "source_paths": [
            "src/graph_generators.py",
            "src/network_analysis.py",
            "src/visualization.py",
        ],
        "functions": [
            graph_generators.build_generative_models,
            network_analysis.compare_generative_models,
        ],
        "image": "generative_models_degree_distribution.png",
        "interactive": None,
    },
    {
        "number": 6,
        "slug": "interactive-color-dashboard",
        "title": "Interactive node-color dashboard",
        "source": "Supplied Section 9 directed social-network pattern",
        "dataset": "outputs/analysis_summary.json",
        "kind": "Interactive dashboard",
        "deliverable": "Plotly network with two fixed-position color modes",
        "source_paths": [
            "src/graph_generators.py",
            "src/visualization.py",
        ],
        "functions": [
            graph_generators.build_social_graph,
            visualization.create_social_toggle_dashboard,
        ],
        "image": None,
        "interactive": "network_color_toggle_dashboard.html",
    },
    {
        "number": 7,
        "slug": "applied-ai-knowledge-graph",
        "title": "Applied AI and Multimedia knowledge graph",
        "source": "Stored synthetic typed-node and semantic-edge CSV files",
        "dataset": "data/generated/domain_graph_nodes.csv",
        "kind": "Knowledge graph",
        "deliverable": "Typed graph, centrality findings, and interactive view",
        "source_paths": [
            "src/graph_generators.py",
            "src/network_analysis.py",
            "src/visualization.py",
        ],
        "functions": [
            graph_generators.load_domain_graph,
            network_analysis.domain_metrics,
        ],
        "image": "domain_graph.png",
        "interactive": "domain_graph.html",
    },
]


def _load_summary() -> dict[str, Any]:
    return json.loads(ANALYSIS_SUMMARY.read_text(encoding="utf-8"))


def _code(functions: list[Callable[..., Any]]) -> str:
    source = "\n\n".join(inspect.getsource(function) for function in functions)
    return html.escape(source)


def _style(prefix: str = "") -> str:
    return f"""
<link rel="icon" href="{prefix}favicon.svg">
<style>
:root{{--ink:#17324d;--paper:#f7f5ef;--coral:#e76f51;--blue:#3973a8;--muted:#607384;--line:#d9e0e5;--card:#fff}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 Arial,sans-serif}}
a{{color:#bd4e35}}a:focus-visible,button:focus-visible{{outline:3px solid #1376a8;outline-offset:3px}}
.wrap{{width:min(1180px,calc(100% - 36px));margin:auto}}nav{{position:sticky;top:0;z-index:10;background:rgba(247,245,239,.97);border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;align-items:center;justify-content:space-between;gap:22px;min-height:68px}}nav a{{text-decoration:none;font-weight:700;color:var(--ink)}}nav .links{{display:flex;gap:18px;flex-wrap:wrap}}
header{{padding:72px 0 54px;background:var(--ink);color:#fff}}header p{{color:#cbd5dc;max-width:800px}}.eyebrow{{text-transform:uppercase;letter-spacing:.13em;font-size:.78rem;font-weight:800;color:var(--coral)}}
h1{{font-size:clamp(2.5rem,6vw,5.2rem);line-height:1.02;letter-spacing:-.045em;margin:.25em 0}}h2{{font-size:clamp(1.8rem,4vw,3rem);line-height:1.12}}h3{{line-height:1.25}}
main section{{padding:54px 0;scroll-margin-top:84px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:0 8px 30px rgba(23,50,77,.05)}}
.card strong.metric{{display:block;font-size:2rem}}.button{{display:inline-block;background:var(--coral);color:#fff!important;text-decoration:none;padding:11px 17px;border-radius:999px;font-weight:800;margin:4px 8px 4px 0}}
.button.secondary{{background:#e8edf1;color:var(--ink)!important}}figure{{margin:28px 0}}img{{display:block;max-width:100%;height:auto;border-radius:14px}}figcaption{{color:var(--muted);font-size:.92rem;margin-top:8px}}
main figure img{{margin-inline:auto;max-height:620px;object-fit:contain}}.feature-figure{{background:#fff;border:1px solid var(--line);border-radius:18px;padding:clamp(14px,2.5vw,28px)}}.feature-figure img{{max-height:460px}}iframe{{width:100%;height:min(58vw,580px);min-height:440px;border:1px solid var(--line);border-radius:14px;background:#fff}}p code{{overflow-wrap:anywhere;word-break:break-word}}pre{{max-width:100%;max-height:680px;overflow:auto;background:#10263a;color:#eaf2f6;border-radius:14px;padding:20px;font:13px/1.55 Consolas,monospace}}pre code{{overflow-wrap:normal;word-break:normal}}
table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{border:1px solid var(--line);padding:9px;text-align:left}}th{{background:#e9eef3}}
.notice{{border-left:5px solid var(--coral);padding:16px 20px;background:#fff}}.exercise-roadmap{{display:grid;gap:16px;counter-reset:exercise}}
.exercise-card{{display:grid;grid-template-columns:82px minmax(0,1fr) auto;align-items:center;gap:24px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;color:var(--ink);text-decoration:none;box-shadow:0 8px 30px rgba(23,50,77,.05);transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}}
.exercise-card:hover{{transform:translateY(-2px);border-color:#b5c6d2;box-shadow:0 14px 36px rgba(23,50,77,.1)}}.exercise-number{{display:grid;place-items:center;width:64px;height:64px;border-radius:50%;background:var(--ink);color:#fff;font:800 1rem/1 Consolas,monospace}}
.exercise-copy h3{{font-size:1.35rem;margin:4px 0 7px}}.exercise-copy p{{color:var(--muted);margin:0}}.exercise-meta{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:3px}}.tag{{display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:999px;padding:4px 9px;color:#506777;background:#f7f9fa;font-size:.72rem;font-weight:800}}
.exercise-cta{{white-space:nowrap;color:#bd4e35;font-weight:800}}.exercise-progress{{display:flex;align-items:center;gap:14px;margin:0 0 24px;color:var(--muted);font-weight:700}}.exercise-progress span{{height:6px;flex:1;border-radius:999px;background:linear-gradient(90deg,var(--coral) var(--progress),#dce3e8 var(--progress))}}
.exercise-nav{{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:0 0 34px}}.exercise-nav a{{font-weight:800;text-decoration:none}}.exercise-nav .next{{text-align:right}}.exercise-nav .all{{color:var(--muted);font-size:.84rem}}
.resource-bar{{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0 8px}}.section-label{{display:block;color:var(--coral);font:800 .75rem/1.3 Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;margin-top:38px;scroll-margin-top:96px}}.exercise-output{{background:#edf3f6;border-radius:16px;padding:20px 24px;margin:18px 0}}.source-list{{display:flex;gap:10px;flex-wrap:wrap;padding:0;list-style:none}}
.source-list a{{display:inline-block;background:#e8edf1;color:var(--ink);text-decoration:none;padding:8px 12px;border-radius:10px;font-weight:800;font-size:.86rem}}
.artifact-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:20px 0}}.artifact-card{{display:flex;flex-direction:column;min-width:0;background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:0 8px 24px rgba(23,50,77,.05)}}.artifact-card h3{{margin:12px 0 4px}}.artifact-card p{{color:var(--muted);margin:0 0 16px}}.artifact-head{{display:flex;align-items:center;justify-content:space-between;gap:12px}}.file-badge{{display:inline-flex;align-items:center;justify-content:center;min-width:70px;border-radius:9px;padding:6px 10px;background:var(--ink);color:#fff;font:800 .76rem/1 Consolas,monospace;letter-spacing:.08em}}.file-size{{color:var(--muted);font-size:.78rem;font-weight:700}}.artifact-link{{margin-top:auto;font-weight:800}}.artifact-note{{color:var(--muted);font-size:.9rem}}footer{{padding:38px 0;background:#11283c;color:#fff}}footer a{{color:#ffab93}}
@media(max-width:850px){{.grid{{grid-template-columns:1fr}}nav .wrap{{align-items:flex-start;padding:12px 0;flex-direction:column}}nav .links{{gap:10px 16px}}iframe{{height:460px;min-height:460px}}pre{{max-height:520px}}.exercise-card{{grid-template-columns:64px minmax(0,1fr)}}.exercise-number{{width:52px;height:52px}}.exercise-cta{{grid-column:2;white-space:normal}}.exercise-nav{{grid-template-columns:1fr 1fr}}.exercise-nav .all{{grid-column:1/-1;grid-row:1;text-align:center}}}}
@media(max-width:650px){{.artifact-grid{{grid-template-columns:1fr}}}}
@media(max-width:520px){{iframe{{height:380px;min-height:380px}}.exercise-card{{grid-template-columns:1fr;gap:12px;padding:20px}}.exercise-number{{width:44px;height:44px}}.exercise-cta{{grid-column:1}}.exercise-nav{{gap:10px;font-size:.82rem}}}}
</style>"""


def _nav(prefix: str = "") -> str:
    return f"""
<nav><div class="wrap"><a href="{prefix}index.html">CSE628 Visual Analytics</a>
<div class="links"><a href="{prefix}index.html#findings">Findings</a>
<a href="{prefix}exercises/index.html">Exercises</a>
<a href="{prefix}methodology.html">Methodology</a>
<a href="{prefix}report/report.pdf">Report</a>
<a href="{REPOSITORY_URL}">GitHub</a></div></div></nav>"""


def _footer(prefix: str = "") -> str:
    return f"""
<footer><div class="wrap"><strong>Visual Analytics and Network Analysis</strong>
<p>{html.escape(STUDENT['name'])} · {html.escape(STUDENT['id'])} ·
{html.escape(STUDENT['university'])}</p>
<p><a href="{prefix}report/report.pdf">PDF report</a> ·
<a href="{prefix}report/report.docx">DOCX report</a> ·
<a href="{prefix}report/report.md">Markdown report</a> ·
<a href="{REPOSITORY_URL}">Source repository</a></p></div></footer>"""


def _page(title: str, body: str, prefix: str = "") -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Academic Facebook engagement and network visualization project">
<title>{html.escape(title)} | CSE628 Visual Analytics</title>{_style(prefix)}</head>
<body>{_nav(prefix)}{body}{_footer(prefix)}</body></html>
"""


def _exercise_result(exercise: dict[str, Any], result: dict[str, Any]) -> str:
    number = exercise["number"]
    if number == 1:
        return (
            f"The {result['nodes']} × {result['nodes']} weighted matrix is symmetric: "
            f"<strong>{result['matrix_symmetric']}</strong>. Total unique route distance "
            f"is {result['total_recorded_distance_km']:,} km."
        )
    if number == 2:
        return (
            f"{result['best_layout']} was selected for this realization. Calculated "
            f"average clustering is {result['average_clustering']:.3f}."
        )
    if number == 3:
        return (
            f"{html.escape(result['most_popular_course'])} has "
            f"{result['most_popular_course_enrollments']} enrollments; "
            f"{html.escape(result['most_enrolled_student'])} takes "
            f"{result['most_enrolled_student_courses']} courses."
        )
    if number == 4:
        return (
            f"{result['edges']} edges use reproducible weights from "
            f"{result['minimum_weight']} to {result['maximum_weight']}."
        )
    if number == 5:
        return html.escape(result["conclusion"])
    if number == 6:
        return (
            f"{result['nodes']} nodes and {result['edges']} directed edges are shown. "
            "Positions remain unchanged between both color modes."
        )
    return (
        f"{html.escape(result['top_betweenness_node'])} has the highest "
        f"inverse-strength weighted betweenness ({result['top_betweenness_value']:.4f})."
    )


def _exercise_limitation(number: int) -> str:
    return {
        1: "The route network is a compact classroom example, not a complete transport system.",
        2: "Layout preference depends on graph scale, labels, parameters, and the analytical task.",
        3: "All people, courses, and enrollments are synthetic teaching records.",
        4: "Random weights demonstrate encoding and do not represent observed tie importance.",
        5: "One small seeded realization per model does not quantify simulation uncertainty.",
        6: "The social graph is synthetic and Plotly line segments do not display arrowheads.",
        7: "The knowledge graph is illustrative and was not extracted from publications.",
    }[number]


def _exercise_filename(exercise: dict[str, Any]) -> str:
    return f"{exercise['number']:02d}-{exercise['slug']}.html"


def _human_file_size(path: Path) -> str:
    size = path.stat().st_size
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / 1024:.0f} KB"


def _exercise_artifact_paths(exercise: dict[str, Any]) -> dict[str, Path | str]:
    number = exercise["number"]
    source_slug = exercise["slug"].replace("-", "_")
    source_folder = ROOT / "exercises" / f"{number:02d}_{source_slug}"
    web_folder = f"{number:02d}-{exercise['slug']}"
    stem = f"exercise_{number:02d}_{source_slug}"
    return {
        "source_folder": source_folder,
        "web_folder": web_folder,
        "python": source_folder / f"{stem}.py",
        "source_notebook": source_folder / f"{stem}.ipynb",
        "executed_notebook": source_folder / f"{stem}_executed.ipynb",
        "html_notebook": source_folder / f"{stem}.html",
    }


def _artifact_card(
    label: str,
    title: str,
    description: str,
    path: Path,
    href: str,
    *,
    preview: bool = False,
) -> str:
    action = "Open in browser" if preview else "Download file"
    attributes = ' target="_blank" rel="noopener"' if preview else " download"
    return f"""
<article class="artifact-card">
  <div class="artifact-head"><span class="file-badge">{html.escape(label)}</span>
  <span class="file-size">{_human_file_size(path)}</span></div>
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(description)}</p>
  <a class="artifact-link" href="{html.escape(href)}"{attributes}>{action} &rarr;</a>
</article>"""


def _exercise_artifact_pack(exercise: dict[str, Any]) -> str:
    paths = _exercise_artifact_paths(exercise)
    web_root = f"../exercise-files/{paths['web_folder']}"
    cards = [
        _artifact_card(
            "PY",
            "Python source",
            "Standalone, reusable implementation generated from the canonical cells.",
            paths["python"],
            f"{web_root}/{paths['python'].name}",
        ),
        _artifact_card(
            "IPYNB",
            "Clean notebook",
            "Editable notebook with code cells ready for a fresh-kernel execution.",
            paths["source_notebook"],
            f"{web_root}/{paths['source_notebook'].name}",
        ),
        _artifact_card(
            "IPYNB+",
            "Executed notebook",
            "The same notebook with verified outputs stored for assessment and review.",
            paths["executed_notebook"],
            f"{web_root}/{paths['executed_notebook'].name}",
        ),
        _artifact_card(
            "HTML",
            "Browser notebook",
            "Standalone HTML export of the executed notebook; no Jupyter installation required.",
            paths["html_notebook"],
            f"{web_root}/{paths['html_notebook'].name}",
            preview=True,
        ),
    ]
    if exercise["interactive"]:
        interactive_path = INTERACTIVE / exercise["interactive"]
        cards.append(
            _artifact_card(
                "PLOTLY",
                "Interactive visualization",
                "Standalone interactive graph with zoom, pan, hover, and responsive sizing.",
                interactive_path,
                f"../interactive/{exercise['interactive']}",
                preview=True,
            )
        )
    return "".join(cards)


def _exercise_card(
    exercise: dict[str, Any],
    result: dict[str, Any],
    href_prefix: str = "",
) -> str:
    filename = _exercise_filename(exercise)
    number = exercise["number"]
    return f"""
<a class="exercise-card" href="{href_prefix}{filename}"
   aria-label="Open Exercise {number}: {html.escape(exercise['title'])}">
  <span class="exercise-number">{number:02d}</span>
  <div class="exercise-copy">
    <span class="exercise-meta">
      <span class="tag">{html.escape(exercise['kind'])}</span>
      <span class="tag">{html.escape(exercise['deliverable'])}</span>
    </span>
    <h3>{html.escape(exercise['title'])}</h3>
    <p>{_exercise_result(exercise, result)}</p>
  </div>
  <span class="exercise-cta">Open complete exercise &rarr;</span>
</a>"""


def _exercise_navigation(number: int) -> str:
    previous_link = ""
    next_link = ""
    if number > 1:
        previous = EXERCISES[number - 2]
        previous_link = (
            f'<a href="{_exercise_filename(previous)}">&larr; Exercise '
            f"{previous['number']:02d}</a>"
        )
    if number < len(EXERCISES):
        following = EXERCISES[number]
        next_link = (
            f'<a class="next" href="{_exercise_filename(following)}">Exercise '
            f"{following['number']:02d} &rarr;</a>"
        )
    return f"""
<div class="exercise-nav">
  <span>{previous_link}</span>
  <a class="all" href="index.html">All seven exercises</a>
  <span>{next_link}</span>
</div>"""


def _write_exercise_pages(summary: dict[str, Any], root: Path) -> None:
    target = root / "exercises"
    target.mkdir(parents=True, exist_ok=True)
    cards = []
    for exercise in EXERCISES:
        number = exercise["number"]
        result = summary["exercises"][f"exercise_{number}"]
        filename = _exercise_filename(exercise)
        cards.append(_exercise_card(exercise, result))
        visual = ""
        if exercise["image"]:
            visual = (
                f'<figure class="feature-figure"><img src="../images/{exercise["image"]}" '
                f'alt="{html.escape(exercise["title"])} visualization">'
                f"<figcaption>Calculated visual output for Exercise {number}.</figcaption></figure>"
            )
        elif exercise["interactive"]:
            visual = (
                f'<iframe title="{html.escape(exercise["title"])}" '
                f'src="../interactive/{exercise["interactive"]}" loading="lazy"></iframe>'
            )
        source_links = "".join(
            f'<li><a href="{REPOSITORY_URL}/blob/main/{path}">'
            f"{html.escape(path)}</a></li>"
            for path in exercise["source_paths"]
        )
        artifact_paths = _exercise_artifact_paths(exercise)
        artifact_pack = _exercise_artifact_pack(exercise)
        progress = number / len(EXERCISES) * 100
        navigation = _exercise_navigation(number)
        body = f"""
<header><div class="wrap"><p class="eyebrow">Exercise {number:02d} · Complete study</p>
<h1>{html.escape(exercise['title'])}</h1><p>{html.escape(exercise['source'])}</p></div></header>
<main><section><div class="wrap">
<div class="exercise-progress">Exercise {number} of {len(EXERCISES)}
<span style="--progress:{progress:.2f}%"></span></div>
{navigation}
<span class="section-label">01 &middot; Objective</span>
<h2>Objective and data source</h2>
<p>The exercise reuses the required teaching definition and saves every calculated
artifact through the deterministic Python pipeline. Relevant data:
<a href="../downloads/{html.escape(exercise['dataset'].replace('/', '__'))}"><code>{html.escape(exercise['dataset'])}</code></a>.</p>
<div class="notice"><strong>Scope:</strong> The Facebook dataset is used for the empirical
analysis. This mandatory network exercise uses the supplied or explicitly synthetic
relationship data because the Facebook table has no verified user-to-user edges.</div>
<div class="resource-bar">
<a class="button" href="../downloads/{html.escape(exercise['dataset'].replace('/', '__'))}">Download exercise data</a>
<a class="button secondary" href="#files">Open file pack</a>
<a class="button secondary" href="{REPOSITORY_URL}/tree/main/exercises/{artifact_paths['source_folder'].name}">Browse exercise folder</a>
<a class="button secondary" href="../report/report.pdf">Read report section</a>
</div>
<span class="section-label" id="files">02 &middot; Files</span>
<h2>Complete exercise file pack</h2>
<p>Use the Python file for reusable source, the clean notebook for independent
execution, the executed notebook for verified outputs, and the HTML edition for
browser review. Every format contains the same exercise logic and evidence.</p>
<div class="artifact-grid">{artifact_pack}</div>
<p class="artifact-note"><strong>Format integrity:</strong> the clean IPYNB has no
stored outputs; the executed IPYNB and HTML were produced by a clean kernel with
errors disallowed.</p>
<span class="section-label">03 &middot; Evidence</span>
<h2>Verified result and visualization</h2>
<div class="exercise-output"><strong>{html.escape(exercise['deliverable'])}</strong>
<p>{_exercise_result(exercise, result)}</p></div>{visual}
<span class="section-label">04 &middot; Reproducibility</span>
<h2>Python implementation</h2>
<p>The implementation below is taken from the canonical project modules. Open any
module to inspect the complete surrounding code and imports.</p>
<ul class="source-list">{source_links}</ul>
<pre><code>{_code(exercise['functions'])}</code></pre>
<span class="section-label">05 &middot; Analysis</span>
<h2>Interpretation and limitation</h2>
<p>{html.escape(result.get('interpretation', result.get('justification', result.get('conclusion', 'The output demonstrates the requested graph representation and visual encoding.'))))}</p>
<p><strong>Limitation:</strong> {html.escape(_exercise_limitation(number))}</p>
{navigation}
</div></section></main>"""
        (target / filename).write_text(
            _page(exercise["title"], body, "../"), encoding="utf-8"
        )
    index_body = f"""
<header><div class="wrap"><p class="eyebrow">Seven mandatory exercises</p>
<h1>Complete network visualization studies.</h1>
<p>Work through the exercises in order. Every step contains its source definition,
data, executable code, visual output, verified finding, interpretation, limitation,
and links to the complete repository.</p></div></header>
<main><section><div class="wrap">
<div class="notice"><strong>Recommended path:</strong> Start with representation,
then compare layouts, construct typed networks, add weights, compare models, and
finish with interactive and knowledge-graph views.</div>
<div class="exercise-roadmap" style="margin-top:24px">{''.join(cards)}</div>
</div></section></main>"""
    (target / "index.html").write_text(
        _page("Exercises", index_body, "../"), encoding="utf-8"
    )


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def generate_static_site(summary: dict[str, Any] | None = None) -> Path:
    """Generate a complete relative-path-safe static website."""

    data = summary or _load_summary()
    if WEBSITE.exists():
        shutil.rmtree(WEBSITE)
    WEBSITE.mkdir(parents=True)
    for directory in (
        "images",
        "interactive",
        "report",
        "data",
        "downloads",
        "exercise-files",
        "visualizations",
    ):
        (WEBSITE / directory).mkdir()
    (WEBSITE / "visualizations" / "interactive").mkdir()

    for image_path in STATIC.glob("*.png"):
        _copy_file(image_path, WEBSITE / "images" / image_path.name)
    for interactive_path in INTERACTIVE.glob("*.html"):
        _copy_file(interactive_path, WEBSITE / "interactive" / interactive_path.name)
        _copy_file(
            interactive_path,
            WEBSITE / "visualizations" / "interactive" / interactive_path.name,
        )
    for exercise in EXERCISES:
        paths = _exercise_artifact_paths(exercise)
        destination = WEBSITE / "exercise-files" / paths["web_folder"]
        for role in (
            "python",
            "source_notebook",
            "executed_notebook",
            "html_notebook",
        ):
            source = paths[role]
            if not source.exists():
                raise FileNotFoundError(f"Missing exercise artifact: {source}")
            _copy_file(source, destination / source.name)
    for suffix in ("md", "docx", "pdf"):
        _copy_file(
            ROOT / "report" / f"report.{suffix}",
            WEBSITE / "report" / f"report.{suffix}",
        )
    _copy_file(ANALYSIS_SUMMARY, WEBSITE / "data" / "analysis_summary.json")
    _copy_file(PROCESSED_CSV, WEBSITE / "data" / PROCESSED_CSV.name)
    _copy_file(ROOT / "public" / "favicon.svg", WEBSITE / "favicon.svg")

    download_paths = {exercise["dataset"] for exercise in EXERCISES} | {
        "data/generated/students.csv",
        "data/generated/courses.csv",
        "data/generated/enrollments.csv",
        "data/generated/domain_graph_edges.csv",
    }
    for relative in sorted(download_paths):
        source = ROOT / relative
        if source.exists():
            _copy_file(
                source,
                WEBSITE / "downloads" / relative.replace("/", "__"),
            )

    engagement = data["engagement"]
    exercise_cards = "".join(
        _exercise_card(
            item,
            data["exercises"][f"exercise_{item['number']}"],
            "exercises/",
        )
        for item in EXERCISES
    )
    body = f"""
<header><div class="wrap"><p class="eyebrow">Facebook engagement × network science</p>
<h1>From post metrics to graph structure.</h1>
<p>A reproducible academic analysis of {engagement['rows']:,} anonymized Facebook posts,
paired with seven complete graph-visualization exercises.</p>
<a class="button" href="#findings">Explore findings</a>
<a class="button secondary" href="report/report.pdf">Read academic report</a></div></header>
<main>
<section id="findings"><div class="wrap"><h2>Evidence-led findings</h2><div class="grid">
<article class="card"><strong class="metric">{engagement['mean_engagement']:,.2f}</strong><p>Mean total engagement, compared with a median of {engagement['median_engagement']:,.0f}.</p></article>
<article class="card"><strong class="metric">{engagement['total_engagement'] / 1_000_000:.2f}M</strong><p>Total recorded reactions, comments, and shares.</p></article>
<article class="card"><strong class="metric">7</strong><p>Mandatory exercises with code, outputs, interpretation, and limitations.</p></article>
</div><figure class="feature-figure"><img src="images/engagement_by_post_type.png" alt="Mean reactions, comments, and shares by Facebook post type">
<figcaption>Mean engagement components by post type. Descriptive differences do not establish causality.</figcaption></figure>
<iframe title="Interactive Facebook engagement explorer" src="interactive/engagement_explorer.html" loading="lazy"></iframe>
</div></section>
<section id="exercises"><div class="wrap"><h2>Seven complete exercises</h2>
<p>Follow the sequence from graph representation to interactive knowledge graphs.
Each step opens a dedicated page with data, code, visual evidence, and analysis.</p>
<div class="exercise-roadmap">{exercise_cards}</div></div></section>
<section><div class="wrap"><h2>Research knowledge graph</h2>
<p>Recommendation Systems is the strongest synthetic bridge by inverse-strength weighted betweenness
({data['exercises']['exercise_7']['top_betweenness_value']:.4f}).</p>
<iframe title="Interactive Applied AI and Multimedia knowledge graph" src="interactive/domain_graph.html" loading="lazy"></iframe></div></section>
</main>"""
    (WEBSITE / "index.html").write_text(
        _page("Facebook Engagement and Network Visual Analytics", body),
        encoding="utf-8",
    )

    method_body = f"""
<header><div class="wrap"><p class="eyebrow">Methodology and integrity</p>
<h1>A pipeline designed to be audited.</h1><p>Raw data, calculated results,
figures, reports, notebooks, and both websites are tied to one deterministic workflow.</p></div></header>
<main><section><div class="wrap">
<h2>Empirical scope</h2><p>The official UCI Facebook Live Sellers in Thailand
CSV is preserved in its original form. Empty placeholder columns are removed,
engagement counts are validated, timestamps are parsed, ratios are zero-safe,
and upper-Tukey outliers are flagged rather than deleted.</p>
<h2>Network scope</h2><p>The Facebook table contains no verified relational
identifiers. It is therefore not converted into a user network. Mandatory graph
exercises use the supplied teaching definitions or clearly labeled synthetic CSV files.</p>
<h2>Reproducibility</h2><pre><code>python main.py
black --check .
ruff check .
pytest
pnpm build
pnpm test</code></pre>
<p><a class="button" href="data/analysis_summary.json">Canonical analytical summary</a>
<a class="button secondary" href="{REPOSITORY_URL}">Complete repository</a></p>
</div></section></main>"""
    (WEBSITE / "methodology.html").write_text(
        _page("Methodology", method_body), encoding="utf-8"
    )
    _write_exercise_pages(data, WEBSITE)

    (WEBSITE / ".nojekyll").write_text("", encoding="utf-8")
    site_manifest = {
        "schema_version": 1,
        "repository_url": REPOSITORY_URL,
        "pages_url": PAGES_URL,
        "exercise_pages": [
            f"exercises/{item['number']:02d}-{item['slug']}.html" for item in EXERCISES
        ],
        "exercise_artifact_folders": [
            f"exercise-files/{item['number']:02d}-{item['slug']}" for item in EXERCISES
        ],
        "canonical_summary": "outputs/analysis_summary.json",
    }
    (WEBSITE / "site_manifest.json").write_text(
        json.dumps(site_manifest, indent=2) + "\n", encoding="utf-8"
    )

    public_pages = PUBLIC / "pages"
    if public_pages.exists():
        shutil.rmtree(public_pages)
    shutil.copytree(WEBSITE, public_pages)
    return WEBSITE
