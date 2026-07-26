"""Reproducible graph definitions adapted from the supplied teaching notebook."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

from src.config import DATA_GENERATED, SEED


def build_transport_graph() -> nx.Graph:
    """Recreate Section 8.2's undirected weighted transportation graph."""

    routes = [
        ("Dhaka", "Chattogram", 264),
        ("Dhaka", "Sylhet", 247),
        ("Dhaka", "Khulna", 209),
        ("Dhaka", "Rajshahi", 256),
        ("Dhaka", "Barishal", 170),
        ("Dhaka", "Rangpur", 300),
        ("Khulna", "Barishal", 130),
        ("Rajshahi", "Rangpur", 130),
        ("Chattogram", "Sylhet", 350),
    ]
    graph = nx.Graph(name="G_transport")
    graph.add_weighted_edges_from(routes)
    return graph


def build_ppi_graph() -> nx.Graph:
    """Recreate Section 8.3's 15-node Watts-Strogatz protein graph."""

    proteins = [f"P{i}" for i in range(1, 16)]
    graph = nx.watts_strogatz_graph(n=len(proteins), k=3, p=0.3, seed=SEED)
    return nx.relabel_nodes(graph, {i: proteins[i] for i in range(len(proteins))})


def build_generative_models() -> dict[str, nx.Graph]:
    """Recreate the three Section 3 models with the original parameters."""

    n_nodes = 30
    return {
        "Erdos-Renyi G(n,p)": nx.erdos_renyi_graph(n=n_nodes, p=0.08, seed=SEED),
        "Watts-Strogatz small-world": nx.watts_strogatz_graph(
            n=n_nodes, k=4, p=0.1, seed=SEED
        ),
        "Barabasi-Albert scale-free": nx.barabasi_albert_graph(
            n=n_nodes, m=2, seed=SEED
        ),
    }


def build_large_ba_graph() -> nx.Graph:
    """Recreate Section 6's 100-node Barabasi-Albert graph."""

    return nx.barabasi_albert_graph(n=100, m=2, seed=SEED)


def add_reproducible_edge_weights(graph: nx.Graph, seed: int = SEED) -> nx.Graph:
    """Copy a graph and assign integer edge weights from 1 through 10."""

    weighted = graph.copy()
    rng = random.Random(seed)
    for source, target in weighted.edges():
        weighted[source][target]["weight"] = rng.randint(1, 10)
    return weighted


def build_social_graph() -> nx.DiGraph:
    """Recreate the seeded directed social graph used by Section 9."""

    rng = random.Random(SEED)
    users = [f"user_{i}" for i in range(1, 21)]
    groups = ["Sports", "Tech", "Music", "Travel"]
    user_group = {user: rng.choice(groups) for user in users}
    edges: list[tuple[str, str]] = []
    for user in users:
        candidate_users = [candidate for candidate in users if candidate != user]
        candidate_weights = [
            3 if user_group[candidate] == user_group[user] else 1
            for candidate in candidate_users
        ]
        chosen = rng.choices(
            candidate_users,
            weights=candidate_weights,
            k=rng.randint(1, 5),
        )
        edges.extend((user, target) for target in sorted(set(chosen)))
    graph = nx.DiGraph(name="G_social")
    graph.add_nodes_from(users)
    graph.add_edges_from(edges)
    nx.set_node_attributes(graph, user_group, "interest_group")
    return graph


def create_student_course_data(output_dir: Path = DATA_GENERATED) -> None:
    """Write deterministic synthetic enrollment tables."""

    students = pd.DataFrame(
        [
            ("S01", "Ayesha Rahman", "Computer Science"),
            ("S02", "Tanvir Ahmed", "Computer Science"),
            ("S03", "Nusrat Jahan", "Software Engineering"),
            ("S04", "Sakib Hasan", "Software Engineering"),
            ("S05", "Farzana Islam", "Data Science"),
            ("S06", "Rafiul Karim", "Data Science"),
            ("S07", "Mehedi Hossain", "Information Systems"),
            ("S08", "Sadia Akter", "Information Systems"),
            ("S09", "Imran Kabir", "Computer Science"),
            ("S10", "Maliha Chowdhury", "Multimedia Technology"),
            ("S11", "Arif Mahmud", "Multimedia Technology"),
            ("S12", "Raisa Noor", "Data Science"),
        ],
        columns=["student_id", "student_name", "major"],
    )
    courses = pd.DataFrame(
        [
            ("C01", "Data Visualization", "Computer Science"),
            ("C02", "Social Network Analysis", "Computer Science"),
            ("C03", "Machine Learning", "Artificial Intelligence"),
            ("C04", "Database Systems", "Computer Science"),
            ("C05", "Human-Computer Interaction", "Multimedia"),
            ("C06", "Research Methodology", "General Studies"),
        ],
        columns=["course_id", "course_name", "department"],
    )
    enrollments = {
        "S01": ["C01", "C02", "C03", "C04"],
        "S02": ["C01", "C02", "C04"],
        "S03": ["C01", "C03", "C05"],
        "S04": ["C01", "C04", "C05"],
        "S05": ["C01", "C02", "C03", "C06"],
        "S06": ["C01", "C02", "C03"],
        "S07": ["C01", "C04", "C06"],
        "S08": ["C01", "C05", "C06"],
        "S09": ["C01", "C02", "C03", "C04", "C06"],
        "S10": ["C01", "C05"],
        "S11": ["C01", "C03", "C05"],
        "S12": ["C01", "C02", "C03", "C06"],
    }
    enrollment_rows = [
        (student, course)
        for student, course_ids in enrollments.items()
        for course in course_ids
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    students.to_csv(output_dir / "students.csv", index=False)
    courses.to_csv(output_dir / "courses.csv", index=False)
    pd.DataFrame(enrollment_rows, columns=["student_id", "course_id"]).to_csv(
        output_dir / "enrollments.csv", index=False
    )


def load_student_course_graph(
    output_dir: Path = DATA_GENERATED,
) -> tuple[nx.Graph, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build the bipartite graph from stored CSV files."""

    students = pd.read_csv(output_dir / "students.csv")
    courses = pd.read_csv(output_dir / "courses.csv")
    enrollments = pd.read_csv(output_dir / "enrollments.csv")
    graph = nx.Graph(name="Synthetic student-course enrollment")
    for record in students.to_dict(orient="records"):
        graph.add_node(
            record["student_id"],
            node_type="student",
            bipartite=0,
            label=record["student_name"],
            major=record["major"],
        )
    for record in courses.to_dict(orient="records"):
        graph.add_node(
            record["course_id"],
            node_type="course",
            bipartite=1,
            label=record["course_name"],
            department=record["department"],
        )
    graph.add_edges_from(enrollments.itertuples(index=False, name=None))
    return graph, students, courses, enrollments


def create_domain_graph_data(output_dir: Path = DATA_GENERATED) -> None:
    """Create a synthetic research knowledge graph for applied AI and multimedia."""

    nodes = pd.DataFrame(
        [
            ("AI", "Artificial Intelligence", "Research area"),
            ("CV", "Computer Vision", "Research area"),
            ("NLP", "Natural Language Processing", "Research area"),
            ("RS", "Recommendation Systems", "Research area"),
            ("HCI", "Human-Computer Interaction", "Research area"),
            ("DL", "Deep Learning", "Method"),
            ("GNN", "Graph Neural Networks", "Method"),
            ("CF", "Collaborative Filtering", "Method"),
            ("Python", "Python", "Tool"),
            ("PyTorch", "PyTorch", "Tool"),
            ("NetworkX", "NetworkX", "Tool"),
            ("EduTech", "Educational Technology", "Application"),
            ("SmartMedia", "Smart Multimedia", "Application"),
            ("Engage", "Engagement Prediction", "Outcome"),
            ("Personalize", "Personalized Content", "Outcome"),
        ],
        columns=["node_id", "label", "node_type"],
    )
    edges = pd.DataFrame(
        [
            ("AI", "CV", "includes", 3),
            ("AI", "NLP", "includes", 3),
            ("AI", "RS", "includes", 3),
            ("CV", "DL", "uses", 3),
            ("NLP", "DL", "uses", 3),
            ("RS", "CF", "uses", 3),
            ("RS", "GNN", "uses", 2),
            ("GNN", "DL", "related_to", 2),
            ("DL", "PyTorch", "implemented_with", 3),
            ("CF", "Python", "implemented_with", 2),
            ("GNN", "NetworkX", "prototyped_with", 2),
            ("HCI", "EduTech", "applied_to", 2),
            ("RS", "EduTech", "applied_to", 3),
            ("CV", "SmartMedia", "applied_to", 3),
            ("NLP", "SmartMedia", "applied_to", 2),
            ("EduTech", "Engage", "generates", 3),
            ("SmartMedia", "Engage", "generates", 2),
            ("RS", "Personalize", "generates", 3),
            ("HCI", "Personalize", "supports", 2),
            ("Python", "NetworkX", "ecosystem_link", 1),
            ("Python", "PyTorch", "ecosystem_link", 1),
        ],
        columns=["source", "target", "relationship", "strength"],
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    nodes.to_csv(output_dir / "domain_graph_nodes.csv", index=False)
    edges.to_csv(output_dir / "domain_graph_edges.csv", index=False)


def load_domain_graph(
    output_dir: Path = DATA_GENERATED,
) -> tuple[nx.Graph, pd.DataFrame, pd.DataFrame]:
    """Build the synthetic research knowledge graph from its CSV tables."""

    nodes = pd.read_csv(output_dir / "domain_graph_nodes.csv")
    edges = pd.read_csv(output_dir / "domain_graph_edges.csv")
    graph = nx.Graph(name="Applied AI and Multimedia Research Knowledge Graph")
    for record in nodes.to_dict(orient="records"):
        graph.add_node(
            record["node_id"],
            label=record["label"],
            node_type=record["node_type"],
        )
    for record in edges.to_dict(orient="records"):
        graph.add_edge(
            record["source"],
            record["target"],
            relationship=record["relationship"],
            weight=int(record["strength"]),
        )
    return graph, nodes, edges


def graph_metrics(graph: nx.Graph) -> dict[str, Any]:
    """Calculate metrics with academically correct disconnected-graph handling."""

    degree_values = np.array([degree for _, degree in graph.degree()], dtype=float)
    is_connected = nx.is_connected(graph)
    components = nx.number_connected_components(graph)
    if is_connected:
        average_path = float(nx.average_shortest_path_length(graph))
        path_scope = "whole graph"
    else:
        largest_nodes = max(nx.connected_components(graph), key=len)
        largest = graph.subgraph(largest_nodes)
        average_path = float(nx.average_shortest_path_length(largest))
        path_scope = "largest connected component"
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": float(nx.density(graph)),
        "average_degree": float(degree_values.mean()),
        "average_clustering": float(nx.average_clustering(graph)),
        "connected": bool(is_connected),
        "connected_components": int(components),
        "average_shortest_path": average_path,
        "average_shortest_path_scope": path_scope,
        "maximum_degree": int(degree_values.max()),
        "degree_standard_deviation": float(degree_values.std(ddof=0)),
    }
