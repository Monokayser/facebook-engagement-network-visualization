import networkx as nx
import numpy as np

from src.graph_generators import build_transport_graph


def test_transport_weighted_matrix_is_symmetric_and_nonbinary():
    graph = build_transport_graph()
    matrix = nx.to_numpy_array(graph, weight="weight")
    assert np.allclose(matrix, matrix.T)
    assert matrix.max() == 350
    assert graph.number_of_nodes() == 7
    assert graph.number_of_edges() == 9
