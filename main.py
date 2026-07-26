"""Run the complete Facebook engagement and network-visualization pipeline."""

from __future__ import annotations

import json
import logging
import shutil
import sys
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

from src.artifact_manifest import build_artifact_manifest
from src.config import (
    ANALYSIS_SUMMARY,
    DATASET,
    EXERCISE_SUMMARIES,
    INTERACTIVE,
    OUTPUTS,
    PROCESSED_CSV,
    PUBLIC,
    RAW_CSV,
    ROOT,
    STATIC,
    STUDENT,
    TABLES,
    WEBSITE,
    ensure_directories,
)
from src.data_loader import load_facebook_data
from src.data_preprocessing import clean_and_engineer, summarize_engagement
from src.graph_generators import (
    add_reproducible_edge_weights,
    build_generative_models,
    build_large_ba_graph,
    build_ppi_graph,
    build_social_graph,
    build_transport_graph,
    create_domain_graph_data,
    create_student_course_data,
    load_domain_graph,
    load_student_course_graph,
)
from src.network_analysis import (
    compare_generative_models,
    domain_metrics,
    student_course_findings,
    transport_representations,
)
from src.notebook_builder import execute_notebooks, generate_notebooks
from src.report_generator import generate_reports
from src.site_generator import generate_static_site
from src.visualization import (
    create_bipartite_figure,
    create_degree_distribution_figures,
    create_domain_interactive,
    create_domain_static,
    create_eda_figures,
    create_engagement_interactive,
    create_layout_figures,
    create_social_toggle_dashboard,
    create_weighted_ba_figures,
)

LOGGER = logging.getLogger("facebook_network_project")


def _json_default(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, Path):
        return value.as_posix()
    raise TypeError(f"Cannot serialize {type(value)}")


def _write_summary_text(filename: str, text: str) -> None:
    path = EXERCISE_SUMMARIES / filename
    path.write_text(text.strip() + "\n", encoding="utf-8")


def _copy_site_assets() -> None:
    for image in STATIC.glob("*.png"):
        shutil.copy2(image, PUBLIC / "images" / image.name)
        destination = WEBSITE / "assets" / image.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image, destination)
    shutil.copy2(PROCESSED_CSV, PUBLIC / "data" / PROCESSED_CSV.name)
    shutil.copy2(ANALYSIS_SUMMARY, PUBLIC / "data" / ANALYSIS_SUMMARY.name)
    for interactive in INTERACTIVE.glob("*.html"):
        shutil.copy2(interactive, PUBLIC / "interactive" / interactive.name)
    for report_name in ("report.md", "report.docx", "report.pdf"):
        source = ROOT / "report" / report_name
        if source.exists():
            shutil.copy2(source, PUBLIC / report_name)


def run_pipeline() -> dict[str, Any]:
    """Generate every analytical, visualization, notebook, and report artifact."""

    ensure_directories()
    raw = load_facebook_data(RAW_CSV)
    processed, audit = clean_and_engineer(raw)
    processed.to_csv(PROCESSED_CSV, index=False)
    engagement = summarize_engagement(processed)
    pd.DataFrame(engagement["by_type"]).to_csv(
        TABLES / "engagement_by_post_type.csv", index=False
    )
    pd.DataFrame(engagement["top_posts"]).to_csv(
        TABLES / "top_10_posts.csv", index=False
    )
    create_eda_figures(processed)
    create_engagement_interactive(processed)

    transport = build_transport_graph()
    matrix, exercise_1 = transport_representations(transport)
    adjacency_lines = "\n".join(
        f"{node}: {', '.join(neighbors)}"
        for node, neighbors in exercise_1["adjacency_list"].items()
    )
    exercise_1_text = (
        "Exercise 1 - Weighted adjacency representations\n"
        f"Adjacency list:\n{adjacency_lines}\n\n"
        f"Symmetric: {exercise_1['matrix_symmetric']}\n{exercise_1['reason']}\n"
    )
    (OUTPUTS / "exercise_01_summary.txt").write_text(exercise_1_text, encoding="utf-8")
    _write_summary_text("exercise_01.txt", exercise_1_text)

    ppi = build_ppi_graph()
    create_layout_figures(ppi)
    exercise_2 = {
        "best_layout": "Kamada-Kawai",
        "justification": (
            "For this exact 15-node realization, Kamada-Kawai minimizes pairwise "
            "distance stress and makes the ring-like locality plus rewired shortcuts "
            "most legible; spring is a close alternative. The measured average "
            "clustering is 0.0, so no layout can reveal triangle-based clustering "
            "that is absent from the supplied k=3 realization."
        ),
        "nodes": ppi.number_of_nodes(),
        "edges": ppi.number_of_edges(),
        "density": float(nx.density(ppi)),
        "connected": bool(nx.is_connected(ppi)),
        "average_degree": float(
            sum(dict(ppi.degree()).values()) / ppi.number_of_nodes()
        ),
        "diameter": int(nx.diameter(ppi)),
        "minimum_degree": int(min(dict(ppi.degree()).values())),
        "maximum_degree": int(max(dict(ppi.degree()).values())),
        "average_clustering": float(nx.average_clustering(ppi)),
    }
    _write_summary_text(
        "exercise_02.txt",
        f"Exercise 2 - Layout comparison\nBest layout: Kamada-Kawai\n"
        f"Measured average clustering: {exercise_2['average_clustering']:.3f}\n"
        f"{exercise_2['justification']}",
    )

    create_student_course_data()
    student_graph, students, courses, _ = load_student_course_graph()
    _, exercise_3 = student_course_findings()
    create_bipartite_figure(student_graph, students, courses)
    _write_summary_text(
        "exercise_03.txt",
        (
            "Exercise 3 - Synthetic student-course bipartite graph\n"
            f"Bipartite: {exercise_3['is_bipartite']}\n"
            f"Most popular course: {exercise_3['most_popular_course']} "
            f"({exercise_3['most_popular_course_enrollments']})\n"
            f"Most enrolled student: {exercise_3['most_enrolled_student']} "
            f"({exercise_3['most_enrolled_student_courses']})\n"
            f"{exercise_3['pattern']}"
        ),
    )

    original_ba = build_large_ba_graph()
    weighted_ba = add_reproducible_edge_weights(original_ba)
    edge_weights = pd.DataFrame(
        [
            {"source": source, "target": target, "weight": data["weight"]}
            for source, target, data in weighted_ba.edges(data=True)
        ]
    )
    edge_weights.to_csv(TABLES / "barabasi_albert_edge_weights.csv", index=False)
    create_weighted_ba_figures(original_ba, weighted_ba)
    exercise_4 = {
        "nodes": original_ba.number_of_nodes(),
        "edges": original_ba.number_of_edges(),
        "minimum_weight": int(edge_weights["weight"].min()),
        "maximum_weight": int(edge_weights["weight"].max()),
        "mean_weight": float(edge_weights["weight"].mean()),
        "median_weight": float(edge_weights["weight"].median()),
        "weight_standard_deviation": float(edge_weights["weight"].std(ddof=0)),
        "total_edge_weight": int(edge_weights["weight"].sum()),
        "average_degree": float(
            sum(dict(original_ba.degree()).values()) / original_ba.number_of_nodes()
        ),
        "maximum_degree": int(max(dict(original_ba.degree()).values())),
        "weight_frequencies": {
            str(int(weight)): int(count)
            for weight, count in edge_weights["weight"]
            .value_counts()
            .sort_index()
            .items()
        },
        "interpretation": (
            "Edge width changes which ties appear salient, but seeded random weights "
            "are an encoding demonstration. Node centrality and edge weight are related "
            "only when the selected centrality definition explicitly uses weights."
        ),
    }
    _write_summary_text(
        "exercise_04.txt",
        (
            "Exercise 4 - Weighted Barabasi-Albert graph\n"
            f"Edges: {exercise_4['edges']}; range: "
            f"{exercise_4['minimum_weight']}-{exercise_4['maximum_weight']}; "
            f"mean: {exercise_4['mean_weight']:.3f}\n"
            f"{exercise_4['interpretation']}"
        ),
    )

    models = build_generative_models()
    comparison, distributions = compare_generative_models(models)
    create_degree_distribution_figures(distributions)
    exercise_5 = {
        "records": comparison.to_dict(orient="records"),
        "conclusion": (
            "Watts-Strogatz captures clustering and short paths; Barabasi-Albert "
            "captures hubs and heterogeneous degree. A social network can require "
            "both properties, so no model is universally best."
        ),
    }
    _write_summary_text(
        "exercise_05.txt",
        f"Exercise 5 - Generative models\n{exercise_5['conclusion']}",
    )

    social = build_social_graph()
    social_path = create_social_toggle_dashboard(social)
    exercise_6 = {
        "nodes": social.number_of_nodes(),
        "edges": social.number_of_edges(),
        "dropdown_modes": ["Interest Group", "In-Degree"],
        "standalone_html": social_path.relative_to(ROOT).as_posix(),
        "positions_preserved": True,
        "directed": True,
        "density": float(nx.density(social)),
        "mean_in_degree": float(
            sum(dict(social.in_degree()).values()) / social.number_of_nodes()
        ),
        "minimum_in_degree": int(min(dict(social.in_degree()).values())),
        "maximum_in_degree": int(max(dict(social.in_degree()).values())),
        "minimum_out_degree": int(min(dict(social.out_degree()).values())),
        "maximum_out_degree": int(max(dict(social.out_degree()).values())),
        "interest_group_counts": {
            group: int(
                sum(
                    data["interest_group"] == group
                    for _, data in social.nodes(data=True)
                )
            )
            for group in sorted(
                {data["interest_group"] for _, data in social.nodes(data=True)}
            )
        },
        "highest_in_degree_users": [
            {"user": user, "in_degree": int(degree)}
            for user, degree in sorted(
                social.in_degree(), key=lambda item: (-item[1], item[0])
            )[:3]
        ],
    }
    _write_summary_text(
        "exercise_06.txt",
        (
            "Exercise 6 - Interactive Plotly dashboard\n"
            "Dropdown modes: Interest Group and In-Degree. Node positions and "
            "edges remain fixed; hover text shows node ID, group, in-degree, and out-degree."
        ),
    )

    create_domain_graph_data()
    domain_graph, _, _ = load_domain_graph()
    _, exercise_7 = domain_metrics()
    create_domain_static(domain_graph)
    domain_path = create_domain_interactive(domain_graph)
    exercise_7["standalone_html"] = domain_path.relative_to(ROOT).as_posix()
    _write_summary_text(
        "exercise_07.txt",
        (
            "Exercise 7 - Synthetic Applied AI and Multimedia research graph\n"
            f"{exercise_7['interpretation']}"
        ),
    )

    summary = {
        "project_title": (
            "Visual Analytics and Network Analysis of Facebook Engagement Using Python"
        ),
        "student": STUDENT,
        "dataset": {
            **DATASET,
            "raw_rows": int(raw.shape[0]),
            "raw_columns": int(raw.shape[1]),
            "processed_rows": int(processed.shape[0]),
            "processed_columns": int(processed.shape[1]),
        },
        "runtime": {
            "python": sys.version.split()[0],
            "seed": 42,
        },
        "data_cleaning": audit,
        "engagement": engagement,
        "exercises": {
            "exercise_1": exercise_1,
            "exercise_2": exercise_2,
            "exercise_3": exercise_3,
            "exercise_4": exercise_4,
            "exercise_5": exercise_5,
            "exercise_6": exercise_6,
            "exercise_7": exercise_7,
        },
        "scope_note": (
            "The real Facebook dataset is analyzed as a table because it contains no "
            "verified user relationship identifiers. Relationship graphs are synthetic."
        ),
    }
    ANALYSIS_SUMMARY.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=_json_default),
        encoding="utf-8",
    )
    notebooks = generate_notebooks()
    generate_reports()
    _copy_site_assets()
    generate_static_site(summary)
    execute_notebooks(notebooks)
    build_artifact_manifest()
    LOGGER.info("Pipeline completed successfully.")
    return summary


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s"
    )
    run_pipeline()
