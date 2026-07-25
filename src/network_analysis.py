"""Numerical analysis for the seven mandatory graph exercises."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

from src.config import TABLES
from src.graph_generators import (
    graph_metrics,
    load_domain_graph,
    load_student_course_graph,
)


def transport_representations(graph: nx.Graph) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Return and save the weighted adjacency representation."""

    nodes = list(graph.nodes())
    matrix = nx.to_pandas_adjacency(graph, nodelist=nodes, weight="weight", dtype=float)
    matrix.index.name = "city"
    symmetric = bool(np.allclose(matrix.to_numpy(), matrix.to_numpy().T))
    matrix.to_csv(TABLES / "g_transport_adjacency_matrix.csv")
    adjacency = {str(node): list(graph.neighbors(node)) for node in nodes}
    weighted_edges = [
        {
            "source": str(source),
            "target": str(target),
            "distance_km": int(data["weight"]),
        }
        for source, target, data in graph.edges(data=True)
    ]
    longest_route = max(weighted_edges, key=lambda edge: edge["distance_km"])
    shortest_route = min(weighted_edges, key=lambda edge: edge["distance_km"])
    return matrix, {
        "adjacency_list": adjacency,
        "matrix_symmetric": symmetric,
        "node_order": nodes,
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": float(nx.density(graph)),
        "weighted_edges": weighted_edges,
        "total_recorded_distance_km": int(
            sum(edge["distance_km"] for edge in weighted_edges)
        ),
        "longest_route": longest_route,
        "shortest_route": shortest_route,
        "highest_degree_city": max(graph.degree, key=lambda item: item[1])[0],
        "highest_degree": int(max(dict(graph.degree()).values())),
        "reason": (
            "Each undirected weighted edge contributes the same weight to cells "
            "(u, v) and (v, u), so the matrix equals its transpose. A directed "
            "graph or asymmetric directional weights would break this symmetry."
        ),
    }


def compare_generative_models(
    models: dict[str, nx.Graph],
) -> tuple[pd.DataFrame, dict[str, list[int]]]:
    """Calculate and save fair statistical comparisons for Section 3 models."""

    rows: list[dict[str, Any]] = []
    distributions: dict[str, list[int]] = {}
    notes = {
        "Erdos-Renyi G(n,p)": (
            "Homogeneous random mixing; limited clustering and no preferential hubs."
        ),
        "Watts-Strogatz small-world": (
            "High local clustering and short paths, but comparatively narrow degrees."
        ),
        "Barabasi-Albert scale-free": (
            "Strong hubs and heterogeneous degrees, but weaker local clustering here."
        ),
    }
    for name, graph in models.items():
        metrics = graph_metrics(graph)
        degrees = [degree for _, degree in graph.degree()]
        distributions[name] = degrees
        rows.append(
            {
                "Model": name,
                "Nodes": metrics["nodes"],
                "Edges": metrics["edges"],
                "Density": metrics["density"],
                "Average Degree": metrics["average_degree"],
                "Average Clustering": metrics["average_clustering"],
                "Connected": metrics["connected"],
                "Connected Components": metrics["connected_components"],
                "Average Shortest Path": metrics["average_shortest_path"],
                "Path Length Scope": metrics["average_shortest_path_scope"],
                "Maximum Degree": metrics["maximum_degree"],
                "Degree Standard Deviation": metrics["degree_standard_deviation"],
                "Social-Network Similarity Notes": notes[name],
            }
        )
    comparison = pd.DataFrame(rows)
    comparison.to_csv(TABLES / "generative_models_comparison.csv", index=False)
    return comparison, distributions


def student_course_findings() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Calculate degree findings for the stored synthetic bipartite dataset."""

    graph, students, courses, _ = load_student_course_graph()
    if not nx.algorithms.bipartite.is_bipartite(graph):
        raise ValueError("Student-course graph is unexpectedly not bipartite")
    records = []
    for node, degree in graph.degree():
        attrs = graph.nodes[node]
        records.append(
            {
                "node_id": node,
                "label": attrs["label"],
                "node_type": attrs["node_type"],
                "degree": degree,
                "major_or_department": attrs.get("major", attrs.get("department")),
            }
        )
    summary = pd.DataFrame(records).sort_values(
        ["node_type", "degree", "node_id"], ascending=[True, False, True]
    )
    summary.to_csv(TABLES / "student_course_degree_summary.csv", index=False)
    course_summary = summary[summary["node_type"] == "course"]
    student_summary = summary[summary["node_type"] == "student"]
    popular = course_summary.loc[course_summary["degree"].idxmax()]
    most_courses = student_summary.loc[student_summary["degree"].idxmax()]
    return summary, {
        "is_bipartite": True,
        "students": int(len(students)),
        "courses": int(len(courses)),
        "enrollments": graph.number_of_edges(),
        "most_popular_course": popular["label"],
        "most_popular_course_enrollments": int(popular["degree"]),
        "most_enrolled_student": most_courses["label"],
        "most_enrolled_student_courses": int(most_courses["degree"]),
        "bipartite_density": float(
            nx.algorithms.bipartite.density(graph, students["student_id"].tolist())
        ),
        "mean_courses_per_student": float(student_summary["degree"].mean()),
        "mean_students_per_course": float(course_summary["degree"].mean()),
        "course_degrees": [
            {"course": row["label"], "enrollments": int(row["degree"])}
            for _, row in course_summary.iterrows()
        ],
        "pattern": (
            "Data Visualization bridges every represented major. Data Science "
            "students also concentrate in Machine Learning and Social Network Analysis, "
            "while Multimedia Technology students favor Human-Computer Interaction."
        ),
    }


def domain_metrics() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Calculate centrality metrics for the synthetic research graph."""

    graph, nodes, _ = load_domain_graph()
    for source, target, data in graph.edges(data=True):
        graph[source][target]["distance"] = 1 / data["weight"]
    degree = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, weight="distance")
    closeness = nx.closeness_centrality(graph)
    pagerank = nx.pagerank(graph, weight="weight")
    records = []
    labels = nodes.set_index("node_id")["label"].to_dict()
    types = nodes.set_index("node_id")["node_type"].to_dict()
    for node in graph:
        records.append(
            {
                "node_id": node,
                "label": labels[node],
                "node_type": types[node],
                "degree": graph.degree(node),
                "degree_centrality": degree[node],
                "betweenness_centrality": betweenness[node],
                "closeness_centrality": closeness[node],
                "pagerank": pagerank[node],
            }
        )
    metrics = pd.DataFrame(records).sort_values(
        "betweenness_centrality", ascending=False
    )
    metrics.to_csv(TABLES / "domain_graph_metrics.csv", index=False)
    top = metrics.iloc[0]
    return metrics, {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "top_betweenness_node": top["label"],
        "top_betweenness_value": float(top["betweenness_centrality"]),
        "connected": bool(nx.is_connected(graph)),
        "average_degree": float(
            sum(dict(graph.degree()).values()) / graph.number_of_nodes()
        ),
        "top_centrality_records": [
            {
                "label": row["label"],
                "node_type": row["node_type"],
                "degree": int(row["degree"]),
                "degree_centrality": float(row["degree_centrality"]),
                "betweenness_centrality": float(row["betweenness_centrality"]),
                "closeness_centrality": float(row["closeness_centrality"]),
                "pagerank": float(row["pagerank"]),
            }
            for _, row in metrics.head(5).iterrows()
        ],
        "interpretation": (
            f"{top['label']} is the strongest bridge by inverse-strength weighted "
            "betweenness, linking research themes, technical methods, and application "
            "outcomes. "
            "The graph is synthetic and demonstrates structural interpretation, "
            "not empirical evidence about a real research community."
        ),
    }
