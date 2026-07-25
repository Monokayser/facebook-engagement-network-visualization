"""Static and interactive visualization generation."""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.lines import Line2D

from src.config import INTERACTIVE, PUBLIC, SEED, STATIC, WEBSITE

COLORS = {
    "navy": "#17324D",
    "blue": "#3973A8",
    "teal": "#2A9D8F",
    "gold": "#E9A23B",
    "coral": "#E76F51",
    "light": "#E9EEF3",
    "gray": "#66788A",
}
TYPE_COLORS = {
    "video": "#2A9D8F",
    "photo": "#3973A8",
    "status": "#E9A23B",
    "link": "#E76F51",
}


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def create_eda_figures(frame: pd.DataFrame) -> list[Path]:
    """Create non-redundant academic EDA figures."""

    created: list[Path] = []
    grouped = (
        frame.groupby("status_type", observed=True)[
            ["num_reactions", "num_comments", "num_shares", "total_engagement"]
        ]
        .mean()
        .sort_values("total_engagement", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, 5.5))
    grouped[["num_reactions", "num_comments", "num_shares"]].plot(
        kind="bar", ax=ax, color=["#3973A8", "#E9A23B", "#2A9D8F"]
    )
    ax.set_title("Mean Facebook Engagement Components by Post Type")
    ax.set_xlabel("Post type")
    ax.set_ylabel("Mean interactions per post")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(["Reactions", "Comments", "Shares"], frameon=False)
    ax.grid(axis="y", color="#D9E0E6", linewidth=0.7)
    path = STATIC / "engagement_by_post_type.png"
    _save(fig, path)
    created.append(path)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for post_type, group in frame.groupby("status_type", observed=True):
        ax.hist(
            np.log1p(group["total_engagement"]),
            bins=35,
            alpha=0.55,
            label=post_type.title(),
            color=TYPE_COLORS[post_type],
        )
    ax.set_title("Distribution of Total Engagement by Post Type")
    ax.set_xlabel("log(1 + total engagement)")
    ax.set_ylabel("Number of posts")
    ax.legend(frameon=False)
    path = STATIC / "engagement_distribution.png"
    _save(fig, path)
    created.append(path)

    variables = ["num_reactions", "num_comments", "num_shares", "total_engagement"]
    corr = frame[variables].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(corr, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(
        range(len(variables)), [item.replace("num_", "") for item in variables]
    )
    ax.set_yticks(
        range(len(variables)), [item.replace("num_", "") for item in variables]
    )
    for row in range(len(variables)):
        for col in range(len(variables)):
            ax.text(
                col,
                row,
                f"{corr.iloc[row, col]:.2f}",
                ha="center",
                va="center",
                color="white" if corr.iloc[row, col] > 0.55 else COLORS["navy"],
            )
    fig.colorbar(image, ax=ax, label="Spearman correlation")
    ax.set_title("Rank Correlation among Engagement Measures")
    path = STATIC / "engagement_correlation.png"
    _save(fig, path)
    created.append(path)

    monthly = (
        frame.set_index("status_published")
        .resample("ME")
        .agg(
            posts=("status_id", "count"),
            median_engagement=("total_engagement", "median"),
        )
    )
    fig, left = plt.subplots(figsize=(10, 5.5))
    right = left.twinx()
    left.plot(
        monthly.index,
        monthly["median_engagement"],
        color=COLORS["blue"],
        linewidth=1.8,
        label="Median engagement",
    )
    right.plot(
        monthly.index,
        monthly["posts"],
        color=COLORS["gold"],
        linewidth=1.2,
        alpha=0.8,
        label="Posts",
    )
    left.set_title("Monthly Posting Activity and Median Engagement")
    left.set_xlabel("Month")
    left.set_ylabel("Median engagement", color=COLORS["blue"])
    right.set_ylabel("Number of posts", color=COLORS["gold"])
    path = STATIC / "monthly_engagement_trend.png"
    _save(fig, path)
    created.append(path)

    hourly = frame.groupby("posting_hour")["total_engagement"].median()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(hourly.index, hourly.values, color=COLORS["teal"])
    ax.set_title("Median Total Engagement by Posting Hour")
    ax.set_xlabel("Posting hour (0-23)")
    ax.set_ylabel("Median engagement")
    ax.set_xticks(range(0, 24, 2))
    ax.grid(axis="y", color="#D9E0E6", linewidth=0.7)
    path = STATIC / "posting_hour_engagement.png"
    _save(fig, path)
    created.append(path)

    return created


def create_layout_figures(graph: nx.Graph) -> dict[str, Path]:
    """Draw G_ppi with the six required layouts using identical encodings."""

    layouts: dict[str, Callable[[], dict]] = {
        "spring": lambda: nx.spring_layout(graph, seed=SEED),
        "circular": lambda: nx.circular_layout(graph),
        "shell": lambda: nx.shell_layout(graph),
        "spectral": lambda: nx.spectral_layout(graph),
        "kamada_kawai": lambda: nx.kamada_kawai_layout(graph),
        "random": lambda: nx.random_layout(graph, seed=SEED),
    }
    degrees = dict(graph.degree())
    sizes = [230 + 165 * degrees[node] for node in graph.nodes()]
    saved: dict[str, Path] = {}

    def draw(ax: plt.Axes, positions: dict, title: str) -> None:
        nx.draw_networkx(
            graph,
            positions,
            ax=ax,
            with_labels=True,
            node_size=sizes,
            node_color="#718F57",
            edge_color="#99A3AD",
            width=1.1,
            font_size=7,
            font_color="white",
        )
        ax.set_title(title.replace("_", " ").title())
        ax.axis("off")

    positions = {name: layout() for name, layout in layouts.items()}
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    for ax, (name, position) in zip(axes.flat, positions.items(), strict=True):
        draw(ax, position, name)
    fig.suptitle(
        "G_ppi Layout Comparison: Identical Graph and Visual Encoding", fontsize=16
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    comparison = STATIC / "g_ppi_layout_comparison.png"
    _save(fig, comparison)
    saved["comparison"] = comparison
    for name, position in positions.items():
        fig, ax = plt.subplots(figsize=(8, 7))
        draw(ax, position, f"G_ppi - {name}")
        path = STATIC / f"g_ppi_{name}_layout.png"
        _save(fig, path)
        saved[name] = path
    return saved


def create_bipartite_figure(
    graph: nx.Graph, students: pd.DataFrame, courses: pd.DataFrame
) -> Path:
    """Draw the stored synthetic enrollment graph."""

    student_nodes = students["student_id"].tolist()
    course_nodes = courses["course_id"].tolist()
    position = nx.bipartite_layout(graph, student_nodes, align="vertical", scale=2)
    labels = nx.get_node_attributes(graph, "label")
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_edges(graph, position, ax=ax, edge_color="#C4CDD5", width=1)
    nx.draw_networkx_nodes(
        graph,
        position,
        nodelist=student_nodes,
        node_shape="o",
        node_color=COLORS["blue"],
        node_size=820,
        ax=ax,
    )
    nx.draw_networkx_nodes(
        graph,
        position,
        nodelist=course_nodes,
        node_shape="s",
        node_color=COLORS["gold"],
        node_size=1100,
        ax=ax,
    )
    nx.draw_networkx_labels(graph, position, labels=labels, font_size=7, ax=ax)
    legend = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLORS["blue"],
            label="Student",
            markersize=11,
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor=COLORS["gold"],
            label="Course",
            markersize=11,
        ),
    ]
    ax.legend(handles=legend, title="Synthetic node type", loc="upper center", ncol=2)
    ax.set_title("Synthetic Student-Course Enrollment Network")
    ax.axis("off")
    path = STATIC / "student_course_bipartite_graph.png"
    _save(fig, path)
    return path


def create_weighted_ba_figures(
    original: nx.Graph, weighted: nx.Graph
) -> tuple[Path, Path]:
    """Draw Section 6's BA graph before and after edge-weight encoding."""

    position = nx.spring_layout(original, seed=SEED, k=0.25)
    degrees = dict(original.degree())
    sizes = [28 + 7 * degrees[node] for node in original.nodes()]
    hubs = set(sorted(degrees, key=degrees.get, reverse=True)[:5])
    node_colors = [
        COLORS["coral"] if node in hubs else COLORS["blue"] for node in original.nodes()
    ]
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx(
        original,
        position,
        ax=ax,
        node_size=sizes,
        node_color=node_colors,
        edge_color="#BCC5CE",
        width=0.55,
        with_labels=False,
    )
    ax.set_title("Section 6 Barabasi-Albert Graph - Unweighted")
    ax.axis("off")
    unweighted_path = STATIC / "barabasi_albert_unweighted.png"
    _save(fig, unweighted_path)

    edge_weights = [weighted[u][v]["weight"] for u, v in weighted.edges()]
    widths = [0.35 + 2.65 * (weight - 1) / 9 for weight in edge_weights]
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx_nodes(
        weighted, position, ax=ax, node_size=sizes, node_color=node_colors
    )
    nx.draw_networkx_edges(
        weighted,
        position,
        ax=ax,
        width=widths,
        edge_color=COLORS["gray"],
        alpha=0.72,
    )
    ax.legend(
        handles=[
            Line2D([0], [0], color=COLORS["gray"], lw=0.6, label="Weight 1"),
            Line2D([0], [0], color=COLORS["gray"], lw=3.0, label="Weight 10"),
        ],
        title="Edge width encoding",
        loc="upper right",
    )
    ax.set_title("Section 6 Barabasi-Albert Graph - Edge Weight 1 to 10")
    ax.axis("off")
    weighted_path = STATIC / "barabasi_albert_weighted.png"
    _save(fig, weighted_path)
    return unweighted_path, weighted_path


def create_degree_distribution_figures(
    distributions: dict[str, list[int]],
) -> list[Path]:
    """Create individual and combined degree-distribution figures."""

    paths: list[Path] = []
    palette = [COLORS["blue"], COLORS["teal"], COLORS["coral"]]
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    for index, ((name, degrees), color) in enumerate(
        zip(distributions.items(), palette, strict=True)
    ):
        bins = np.arange(min(degrees) - 0.5, max(degrees) + 1.5)
        axes[index].hist(degrees, bins=bins, color=color, edgecolor="white")
        axes[index].set_title(name, fontsize=10)
        axes[index].set_xlabel("Degree")
        axes[index].set_ylabel("Nodes")
        individual, individual_ax = plt.subplots(figsize=(7, 5))
        individual_ax.hist(degrees, bins=bins, color=color, edgecolor="white")
        individual_ax.set_title(f"Degree Distribution - {name}")
        individual_ax.set_xlabel("Degree")
        individual_ax.set_ylabel("Number of nodes")
        path = STATIC / f"model_{index + 1}_degree_distribution.png"
        _save(individual, path)
        paths.append(path)
    fig.suptitle("Degree Distributions of the Three Section 3 Generative Models")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    combined = STATIC / "generative_models_degree_distribution.png"
    _save(fig, combined)
    paths.append(combined)
    return paths


def create_domain_static(graph: nx.Graph) -> Path:
    """Draw the synthetic applied-AI research knowledge graph."""

    position = nx.spring_layout(graph, seed=SEED, weight="weight", k=0.8)
    type_colors = {
        "Research area": COLORS["blue"],
        "Method": COLORS["teal"],
        "Tool": COLORS["gold"],
        "Application": COLORS["coral"],
        "Outcome": "#8767A6",
    }
    colors = [type_colors[graph.nodes[node]["node_type"]] for node in graph]
    sizes = [600 + 350 * graph.degree(node) for node in graph]
    widths = [0.6 + graph[u][v]["weight"] * 0.65 for u, v in graph.edges()]
    labels = nx.get_node_attributes(graph, "label")
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx(
        graph,
        position,
        labels=labels,
        node_color=colors,
        node_size=sizes,
        edge_color="#AAB4BD",
        width=widths,
        font_size=7,
        ax=ax,
    )
    ax.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=color,
                label=kind,
                markersize=10,
            )
            for kind, color in type_colors.items()
        ],
        title="Synthetic node type",
        loc="upper left",
    )
    ax.set_title("Synthetic Research Knowledge Graph for Applied AI and Multimedia")
    ax.axis("off")
    path = STATIC / "domain_graph.png"
    _save(fig, path)
    return path


def _write_interactive(fig: go.Figure, filename: str) -> Path:
    path = INTERACTIVE / filename
    fig.write_html(
        path,
        include_plotlyjs=True,
        full_html=True,
        config={"responsive": True, "displaylogo": False},
    )
    for destination in (
        PUBLIC / "interactive" / filename,
        WEBSITE / filename,
    ):
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    return path


def create_social_toggle_dashboard(graph: nx.DiGraph) -> Path:
    """Create the required Plotly dropdown for interest group versus in-degree."""

    position = nx.spring_layout(graph, seed=SEED, k=0.6)
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for source, target in graph.edges():
        x0, y0 = position[source]
        x1, y1 = position[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    traces: list[go.Scatter] = [
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line={"width": 0.8, "color": "#AAB4BD"},
            hoverinfo="skip",
            name="Follows",
            showlegend=False,
        )
    ]
    group_colors = {
        "Sports": "#3973A8",
        "Tech": "#2A9D8F",
        "Music": "#E76F51",
        "Travel": "#8767A6",
    }
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())
    for group, color in group_colors.items():
        nodes = [node for node in graph if graph.nodes[node]["interest_group"] == group]
        traces.append(
            go.Scatter(
                x=[position[node][0] for node in nodes],
                y=[position[node][1] for node in nodes],
                mode="markers",
                name=group,
                visible=True,
                text=[
                    (
                        f"<b>{node}</b><br>Interest group: {group}"
                        f"<br>In-degree: {in_degree[node]}"
                        f"<br>Out-degree: {out_degree[node]}"
                    )
                    for node in nodes
                ],
                hoverinfo="text",
                marker={
                    "size": [14 + 3 * in_degree[node] for node in nodes],
                    "color": color,
                    "line": {"width": 1, "color": "white"},
                },
            )
        )
    nodes = list(graph.nodes())
    traces.append(
        go.Scatter(
            x=[position[node][0] for node in nodes],
            y=[position[node][1] for node in nodes],
            mode="markers",
            name="In-degree",
            visible=False,
            text=[
                (
                    f"<b>{node}</b><br>Interest group: "
                    f"{graph.nodes[node]['interest_group']}"
                    f"<br>In-degree: {in_degree[node]}"
                    f"<br>Out-degree: {out_degree[node]}"
                )
                for node in nodes
            ],
            hoverinfo="text",
            marker={
                "size": [14 + 3 * in_degree[node] for node in nodes],
                "color": [in_degree[node] for node in nodes],
                "colorscale": "Viridis",
                "showscale": True,
                "colorbar": {"title": "In-degree"},
                "line": {"width": 1, "color": "white"},
            },
        )
    )
    interest_visibility = [True, True, True, True, True, False]
    degree_visibility = [True, False, False, False, False, True]
    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Directed Social Network - Color by Interest Group",
        template="plotly_white",
        hovermode="closest",
        margin={"l": 20, "r": 20, "t": 90, "b": 20},
        xaxis={"visible": False},
        yaxis={"visible": False},
        height=700,
        legend={"orientation": "h", "y": -0.05},
        updatemenus=[
            {
                "type": "dropdown",
                "direction": "down",
                "x": 0.01,
                "y": 1.12,
                "buttons": [
                    {
                        "label": "Color by Interest Group",
                        "method": "update",
                        "args": [
                            {"visible": interest_visibility},
                            {
                                "title": "Directed Social Network - Color by Interest Group"
                            },
                        ],
                    },
                    {
                        "label": "Color by In-Degree",
                        "method": "update",
                        "args": [
                            {"visible": degree_visibility},
                            {"title": "Directed Social Network - Color by In-Degree"},
                        ],
                    },
                ],
            }
        ],
    )
    return _write_interactive(fig, "network_color_toggle_dashboard.html")


def create_domain_interactive(graph: nx.Graph) -> Path:
    """Create a hover-rich interactive version of the synthetic domain graph."""

    position = nx.spring_layout(graph, seed=SEED, weight="weight", k=0.8)
    degree = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, weight="weight")
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for source, target in graph.edges():
        edge_x.extend([position[source][0], position[target][0], None])
        edge_y.extend([position[source][1], position[target][1], None])
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line={"width": 1.2, "color": "#B5BEC7"},
        hoverinfo="skip",
    )
    nodes = list(graph.nodes())
    node_trace = go.Scatter(
        x=[position[node][0] for node in nodes],
        y=[position[node][1] for node in nodes],
        mode="markers+text",
        text=[graph.nodes[node]["label"] for node in nodes],
        textposition="top center",
        hovertext=[
            (
                f"<b>{graph.nodes[node]['label']}</b>"
                f"<br>Type: {graph.nodes[node]['node_type']}"
                f"<br>Degree: {graph.degree(node)}"
                f"<br>Degree centrality: {degree[node]:.3f}"
                f"<br>Betweenness: {betweenness[node]:.3f}"
            )
            for node in nodes
        ],
        hoverinfo="text",
        marker={
            "size": [18 + 42 * degree[node] for node in nodes],
            "color": [betweenness[node] for node in nodes],
            "colorscale": "Tealgrn",
            "showscale": True,
            "colorbar": {"title": "Betweenness"},
            "line": {"width": 1, "color": "white"},
        },
    )
    fig = go.Figure([edge_trace, node_trace])
    fig.update_layout(
        title="Synthetic Applied AI and Multimedia Research Knowledge Graph",
        template="plotly_white",
        height=720,
        margin={"l": 20, "r": 20, "t": 70, "b": 20},
        xaxis={"visible": False},
        yaxis={"visible": False},
        showlegend=False,
    )
    return _write_interactive(fig, "domain_graph.html")


def create_engagement_interactive(frame: pd.DataFrame) -> Path:
    """Create an interactive post-level engagement explorer."""

    traces = []
    for post_type, group in frame.groupby("status_type", observed=True):
        traces.append(
            go.Scattergl(
                x=group["num_reactions"],
                y=group["num_comments"] + group["num_shares"],
                mode="markers",
                name=post_type.title(),
                text=[
                    (
                        f"Post ID: {row.status_id}<br>Published: {row.status_published}"
                        f"<br>Total engagement: {row.total_engagement:,}"
                        f"<br>Shares: {row.num_shares:,}"
                    )
                    for row in group.itertuples()
                ],
                hoverinfo="text",
                marker={
                    "size": np.clip(
                        5 + np.log1p(group["total_engagement"]) * 1.2, 6, 18
                    ),
                    "color": TYPE_COLORS[post_type],
                    "opacity": 0.55,
                },
            )
        )
    fig = go.Figure(traces)
    fig.update_layout(
        title="Facebook Post Engagement Explorer",
        xaxis_title="Reactions (log scale)",
        yaxis_title="Comments + shares (log scale)",
        xaxis_type="log",
        yaxis_type="log",
        template="plotly_white",
        height=680,
        legend_title="Post type",
        margin={"l": 60, "r": 20, "t": 70, "b": 60},
    )
    return _write_interactive(fig, "engagement_explorer.html")
