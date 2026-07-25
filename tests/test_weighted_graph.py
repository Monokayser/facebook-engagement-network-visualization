from src.graph_generators import add_reproducible_edge_weights, build_large_ba_graph


def test_ba_weights_are_reproducible_and_in_range():
    original = build_large_ba_graph()
    first = add_reproducible_edge_weights(original)
    second = add_reproducible_edge_weights(original)
    weights = [data["weight"] for _, _, data in first.edges(data=True)]
    assert original.number_of_nodes() == 100
    assert original.number_of_edges() == 196
    assert min(weights) == 1
    assert max(weights) == 10
    assert weights == [data["weight"] for _, _, data in second.edges(data=True)]
