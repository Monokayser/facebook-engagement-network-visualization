import networkx as nx

from src.graph_generators import (
    create_student_course_data,
    load_student_course_graph,
)


def test_student_course_graph_is_bipartite():
    create_student_course_data()
    graph, students, courses, enrollments = load_student_course_graph()
    assert nx.algorithms.bipartite.is_bipartite(graph)
    assert len(students) == 12
    assert len(courses) == 6
    assert len(enrollments) == graph.number_of_edges() == 40
