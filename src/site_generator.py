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
main section{{padding:54px 0}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:0 8px 30px rgba(23,50,77,.05)}}
.card strong.metric{{display:block;font-size:2rem}}.button{{display:inline-block;background:var(--coral);color:#fff!important;text-decoration:none;padding:11px 17px;border-radius:999px;font-weight:800;margin:4px 8px 4px 0}}
.button.secondary{{background:#e8edf1;color:var(--ink)!important}}figure{{margin:28px 0}}img{{display:block;max-width:100%;height:auto;border-radius:14px}}figcaption{{color:var(--muted);font-size:.92rem;margin-top:8px}}
iframe{{width:100%;min-height:720px;border:1px solid var(--line);border-radius:14px;background:#fff}}pre{{overflow:auto;background:#10263a;color:#eaf2f6;border-radius:14px;padding:20px;font:13px/1.55 Consolas,monospace}}
table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{border:1px solid var(--line);padding:9px;text-align:left}}th{{background:#e9eef3}}
.notice{{border-left:5px solid var(--coral);padding:16px 20px;background:#fff}}footer{{padding:38px 0;background:#11283c;color:#fff}}footer a{{color:#ffab93}}
@media(max-width:850px){{.grid{{grid-template-columns:1fr}}nav .wrap{{align-items:flex-start;padding:12px 0;flex-direction:column}}iframe{{min-height:580px}}}}
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


def _write_exercise_pages(summary: dict[str, Any], root: Path) -> None:
    target = root / "exercises"
    target.mkdir(parents=True, exist_ok=True)
    cards = []
    for exercise in EXERCISES:
        number = exercise["number"]
        result = summary["exercises"][f"exercise_{number}"]
        filename = f"{number:02d}-{exercise['slug']}.html"
        cards.append(
            f'<article class="card"><span class="eyebrow">Exercise {number:02d}</span>'
            f"<h3>{html.escape(exercise['title'])}</h3>"
            f"<p>{_exercise_result(exercise, result)}</p>"
            f'<a href="{filename}">Open complete exercise →</a></article>'
        )
        visual = ""
        if exercise["image"]:
            visual = (
                f'<figure><img src="../images/{exercise["image"]}" '
                f'alt="{html.escape(exercise["title"])} visualization">'
                f"<figcaption>Calculated visual output for Exercise {number}.</figcaption></figure>"
            )
        elif exercise["interactive"]:
            visual = (
                f'<iframe title="{html.escape(exercise["title"])}" '
                f'src="../interactive/{exercise["interactive"]}" loading="lazy"></iframe>'
            )
        body = f"""
<header><div class="wrap"><p class="eyebrow">Exercise {number:02d} · Complete study</p>
<h1>{html.escape(exercise['title'])}</h1><p>{html.escape(exercise['source'])}</p></div></header>
<main><section><div class="wrap"><h2>Objective and data source</h2>
<p>The exercise reuses the required teaching definition and saves every calculated
artifact through the deterministic Python pipeline. Relevant data:
<a href="../downloads/{html.escape(exercise['dataset'].replace('/', '__'))}"><code>{html.escape(exercise['dataset'])}</code></a>.</p>
<div class="notice"><strong>Scope:</strong> The Facebook dataset is used for the empirical
analysis. This mandatory network exercise uses the supplied or explicitly synthetic
relationship data because the Facebook table has no verified user-to-user edges.</div>
<h2>Verified result</h2><p>{_exercise_result(exercise, result)}</p>{visual}
<h2>Python implementation</h2><pre><code>{_code(exercise['functions'])}</code></pre>
<p><a class="button" href="{REPOSITORY_URL}/tree/main/src">Browse complete Python source</a>
<a class="button secondary" href="../report/report.pdf">Read report section</a></p>
<h2>Interpretation and limitation</h2>
<p>{html.escape(result.get('interpretation', result.get('justification', result.get('conclusion', 'The output demonstrates the requested graph representation and visual encoding.'))))}</p>
<p><strong>Limitation:</strong> {html.escape(_exercise_limitation(number))}</p>
</div></section></main>"""
        (target / filename).write_text(
            _page(exercise["title"], body, "../"), encoding="utf-8"
        )
    index_body = f"""
<header><div class="wrap"><p class="eyebrow">Seven mandatory exercises</p>
<h1>Complete network visualization studies.</h1>
<p>Each page provides the required source definition, code, output, interpretation,
limitation, and downloadable evidence.</p></div></header>
<main><section><div class="wrap"><div class="grid">{''.join(cards)}</div></div></section></main>"""
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
    for directory in ("images", "interactive", "report", "data", "downloads"):
        (WEBSITE / directory).mkdir()

    for image_path in STATIC.glob("*.png"):
        _copy_file(image_path, WEBSITE / "images" / image_path.name)
    for interactive_path in INTERACTIVE.glob("*.html"):
        _copy_file(interactive_path, WEBSITE / "interactive" / interactive_path.name)
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
        f'<article class="card"><span class="eyebrow">Exercise {item["number"]:02d}</span>'
        f'<h3>{html.escape(item["title"])}</h3>'
        f"<p>{_exercise_result(item, data['exercises'][f'exercise_{item['number']}'])}</p>"
        f'<a href="exercises/{item["number"]:02d}-{item["slug"]}.html">Code, output and analysis →</a></article>'
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
</div><figure><img src="images/engagement_by_post_type.png" alt="Mean reactions, comments, and shares by Facebook post type">
<figcaption>Mean engagement components by post type. Descriptive differences do not establish causality.</figcaption></figure>
<iframe title="Interactive Facebook engagement explorer" src="interactive/engagement_explorer.html" loading="lazy"></iframe>
</div></section>
<section id="exercises"><div class="wrap"><h2>Seven complete exercises</h2><div class="grid">{exercise_cards}</div></div></section>
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
