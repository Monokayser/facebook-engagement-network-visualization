import networkx as nx

from src.graph_generators import build_generative_models, graph_metrics


def test_model_metrics_handle_disconnected_graphs():
    comparison = {
        name: graph_metrics(graph) for name, graph in build_generative_models().items()
    }
    erdos = comparison["Erdos-Renyi G(n,p)"]
    assert erdos["connected"] is False
    assert erdos["connected_components"] == 3
    assert erdos["average_shortest_path_scope"] == "largest connected component"
    assert all(metrics["nodes"] == 30 for metrics in comparison.values())


def test_graph_metrics_connected_scope():
    metrics = graph_metrics(nx.path_graph(5))
    assert metrics["connected"] is True
    assert metrics["average_shortest_path_scope"] == "whole graph"
    assert metrics["average_shortest_path"] == 2.0
