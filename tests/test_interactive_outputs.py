from src.config import INTERACTIVE, STATIC


def test_required_static_and_interactive_outputs_exist():
    required = [
        STATIC / "g_ppi_layout_comparison.png",
        STATIC / "student_course_bipartite_graph.png",
        STATIC / "barabasi_albert_weighted.png",
        STATIC / "domain_graph.png",
        INTERACTIVE / "network_color_toggle_dashboard.html",
        INTERACTIVE / "domain_graph.html",
        INTERACTIVE / "engagement_explorer.html",
    ]
    assert all(path.exists() and path.stat().st_size > 10_000 for path in required)


def test_network_dropdown_labels_are_embedded():
    html = (INTERACTIVE / "network_color_toggle_dashboard.html").read_text(
        encoding="utf-8"
    )
    assert "Color by Interest Group" in html
    assert "Color by In-Degree" in html
    assert "updatemenus" in html
