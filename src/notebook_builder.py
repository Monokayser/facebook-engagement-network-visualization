"""Build and execute the project notebooks from canonical analytical outputs."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from src.config import NOTEBOOKS, ROOT, STUDENT


def _base_cells(title: str, purpose: str) -> list:
    return [
        nbformat.v4.new_markdown_cell(
            f"# {title}\n\n{purpose}\n\n"
            f"**Student:** {STUDENT['name']} ({STUDENT['id']})  \n"
            f"**Course:** {STUDENT['course_name']} ({STUDENT['course_code']}), "
            f"{STUDENT['semester']}\n\n"
            "All paths are project-relative and all reported values are calculated "
            "from the stored data or `outputs/analysis_summary.json`."
        ),
        nbformat.v4.new_code_cell(
            "from pathlib import Path\n"
            "import json\n"
            "import sys\n"
            "from IPython.display import Image, display\n"
            "ROOT = Path.cwd().resolve()\n"
            "if ROOT.name == 'notebooks':\n"
            "    ROOT = ROOT.parent\n"
            "if str(ROOT) not in sys.path:\n"
            "    sys.path.insert(0, str(ROOT))\n"
            "SUMMARY = json.loads((ROOT / 'outputs' / 'analysis_summary.json').read_text(encoding='utf-8'))\n"
            "print('Project root resolved successfully.')\n"
            "print('Canonical summary: outputs/analysis_summary.json')"
        ),
    ]


def _exercise_cells() -> list:
    """Return explicit code and interpretation cells for all seven exercises."""

    return [
        nbformat.v4.new_markdown_cell(
            "## Exercise 1 - Weighted adjacency representations\n\n"
            "**Objective.** Recreate the supplied `G_transport` graph, print its "
            "adjacency list, calculate the weighted matrix, and test symmetry."
        ),
        nbformat.v4.new_code_cell(
            "import numpy as np\n"
            "from src.graph_generators import build_transport_graph\n"
            "from src.network_analysis import transport_representations\n"
            "G_transport = build_transport_graph()\n"
            "transport_matrix, transport_result = transport_representations(G_transport)\n"
            "print('Adjacency list:')\n"
            "for node, neighbours in transport_result['adjacency_list'].items():\n"
            "    print(f'{node}: {neighbours}')\n"
            "display(transport_matrix)\n"
            "print('Symmetric:', np.allclose(transport_matrix, transport_matrix.T))"
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** The matrix is symmetric because every route is "
            "undirected and has one shared distance. A directed or direction-dependent "
            "transport graph could produce an asymmetric matrix.\n\n"
            "**Limitation.** The seven-city graph is a teaching example rather than a "
            "complete or geographically validated route network."
        ),
        nbformat.v4.new_markdown_cell(
            "## Exercise 2 - Six-layout comparison\n\n"
            "**Objective.** Compare spring, circular, shell, spectral, "
            "Kamada-Kawai, and random placement while holding topology and styling fixed."
        ),
        nbformat.v4.new_code_cell(
            "from IPython.display import Image, display\n"
            "from src.graph_generators import build_ppi_graph, graph_metrics\n"
            "G_ppi = build_ppi_graph()\n"
            "display(graph_metrics(G_ppi))\n"
            "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'g_ppi_layout_comparison.png')))"
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** Kamada-Kawai gives the clearest distance-oriented view "
            "of ring locality and rewired shortcuts for this realization. The calculated "
            "clustering coefficient is 0.000, so no layout can establish triangle-based "
            "clusters that are absent from the graph.\n\n"
            "**Limitation.** Layout preference depends on topology, scale, labels, and "
            "the reader's task; it is not a universal ranking."
        ),
        nbformat.v4.new_markdown_cell(
            "## Exercise 3 - Student-course bipartite network\n\n"
            "**Objective.** Build a two-mode graph from stored synthetic CSV tables and "
            "identify course popularity and student course load."
        ),
        nbformat.v4.new_code_cell(
            "import networkx as nx\n"
            "from src.graph_generators import load_student_course_graph\n"
            "from src.network_analysis import student_course_findings\n"
            "student_graph, students, courses, enrollments = load_student_course_graph()\n"
            "degree_table, student_result = student_course_findings()\n"
            "print('Bipartite:', nx.algorithms.bipartite.is_bipartite(student_graph))\n"
            "display(degree_table)\n"
            "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'student_course_bipartite_graph.png')))"
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** Degree represents course load for student nodes and "
            "synthetic popularity for course nodes. These meanings must not be conflated.\n\n"
            "**Limitation.** Names, majors, courses, and enrollments are illustrative and "
            "do not describe actual Daffodil International University records."
        ),
        nbformat.v4.new_markdown_cell(
            "## Exercise 4 - Weighted Barabasi-Albert graph\n\n"
            "**Objective.** Assign reproducible integer edge weights from 1 to 10 and "
            "encode them through line width without changing topology."
        ),
        nbformat.v4.new_code_cell(
            "import pandas as pd\n"
            "weights = pd.read_csv(ROOT / 'outputs' / 'tables' / 'barabasi_albert_edge_weights.csv')\n"
            "display(weights.head(10))\n"
            "display(weights['weight'].describe())\n"
            "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'barabasi_albert_weighted.png')))"
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** Width changes the salience of selected ties, but random "
            "edge weights do not redefine which nodes are degree hubs. A weighted "
            "centrality measure would require a justified strength or distance meaning.\n\n"
            "**Limitation.** The weights demonstrate visual encoding only."
        ),
        nbformat.v4.new_markdown_cell(
            "## Exercise 5 - Generative-model statistics\n\n"
            "**Objective.** Compare the exact seeded Erdos-Renyi, Watts-Strogatz, and "
            "Barabasi-Albert realizations using consistent structural metrics."
        ),
        nbformat.v4.new_code_cell(
            "from src.graph_generators import build_generative_models\n"
            "from src.network_analysis import compare_generative_models\n"
            "model_table, distributions = compare_generative_models(build_generative_models())\n"
            "display(model_table)\n"
            "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'generative_models_degree_distribution.png')))"
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** Watts-Strogatz better represents clustering and short "
            "paths, whereas Barabasi-Albert better represents hubs and heterogeneous "
            "degree. Neither is universally closest to every social network.\n\n"
            "**Limitation.** One small realization per model cannot characterize the "
            "full sampling distribution of the metrics."
        ),
        nbformat.v4.new_markdown_cell(
            "## Exercise 6 - Interactive node-color dashboard\n\n"
            "**Objective.** Preserve node positions while toggling color between "
            "categorical interest group and continuous in-degree."
        ),
        nbformat.v4.new_code_cell(
            "from IPython.display import HTML, display\n"
            "dashboard_path = ROOT / 'visualizations' / 'interactive' / 'network_color_toggle_dashboard.html'\n"
            "dashboard_html = dashboard_path.read_text(encoding='utf-8')\n"
            "print('Standalone size:', f'{dashboard_path.stat().st_size / 1024:.1f} KiB')\n"
            "print('Dropdown labels present:', all(label in dashboard_html for label in ['Color by Interest Group', 'Color by In-Degree']))\n"
            'display(HTML(\'<a href="../visualizations/interactive/network_color_toggle_dashboard.html" target="_blank">Open standalone dashboard</a>\'))'
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** Fixed coordinates isolate the effect of color: the "
            "categorical view supports group-mixing inspection and the continuous view "
            "emphasizes incoming-tie popularity.\n\n"
            "**Limitation.** Plotly line traces do not show arrowheads; direction is "
            "communicated through in-degree and out-degree values."
        ),
        nbformat.v4.new_markdown_cell(
            "## Exercise 7 - Applied AI and Multimedia knowledge graph\n\n"
            "**Objective.** Build a typed, weighted graph from CSV files and calculate "
            "degree, inverse-strength betweenness, closeness, and PageRank."
        ),
        nbformat.v4.new_code_cell(
            "from src.network_analysis import domain_metrics\n"
            "domain_table, domain_result = domain_metrics()\n"
            "display(domain_table.head(10))\n"
            "print('Top bridge:', domain_result['top_betweenness_node'], domain_result['top_betweenness_value'])\n"
            "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'domain_graph.png')))"
        ),
        nbformat.v4.new_markdown_cell(
            "**Interpretation.** Recommendation Systems is the strongest bridge under "
            "inverse-strength weighted betweenness because it connects research themes, "
            "methods, and application outcomes.\n\n"
            "**Limitation.** The graph is illustrative and is not evidence extracted "
            "from publications or a real research community."
        ),
    ]


def generate_notebooks() -> list[Path]:
    """Write the six requested notebooks with explicit analytical narratives."""

    specs = [
        (
            "01_data_understanding.ipynb",
            "Data Understanding",
            "Inspect the official UCI Facebook dataset without changing the raw file.",
            [
                nbformat.v4.new_markdown_cell(
                    "## Provenance and analytical scope\n\n"
                    "The dataset records post-level engagement for ten anonymized Thai "
                    "Facebook seller pages. It supports tabular engagement analysis but "
                    "does not contain verified user-to-user relationships."
                ),
                nbformat.v4.new_code_cell(
                    "from src.config import RAW_CSV\n"
                    "from src.data_loader import load_facebook_data\n"
                    "raw = load_facebook_data(RAW_CSV)\n"
                    "print('Shape:', raw.shape)\n"
                    "display(raw.head())\n"
                    "display(raw.dtypes.rename('dtype').to_frame())\n"
                    "display(raw.isna().sum().rename('missing').to_frame())"
                ),
                nbformat.v4.new_markdown_cell(
                    "Four placeholder columns are completely empty. Engagement counts "
                    "are nonnegative, timestamps require parsing, and status type is the "
                    "principal categorical comparison variable."
                ),
            ],
        ),
        (
            "02_data_cleaning.ipynb",
            "Data Cleaning and Feature Engineering",
            "Apply the modular transformation workflow and inspect its audit trail.",
            [
                nbformat.v4.new_code_cell(
                    "from src.config import RAW_CSV\n"
                    "from src.data_loader import load_facebook_data\n"
                    "from src.data_preprocessing import clean_and_engineer, validate_processed\n"
                    "processed, audit = clean_and_engineer(load_facebook_data(RAW_CSV))\n"
                    "validate_processed(processed)\n"
                    "display(audit)\n"
                    "display(processed.head())"
                ),
                nbformat.v4.new_code_cell(
                    "engineered = ['reaction_components_total', 'total_engagement', "
                    "'like_to_comment_ratio', 'share_to_engagement_ratio', "
                    "'positive_reaction_percentage', 'posting_hour', 'day_of_week', "
                    "'month', 'is_weekend', 'time_of_day', 'engagement_category', "
                    "'engagement_outlier']\n"
                    "display(processed[engineered].describe(include='all').T)"
                ),
                nbformat.v4.new_markdown_cell(
                    "Outliers are flagged rather than deleted. Ratio calculations are "
                    "zero-safe, and no engagement-rate claim is made because reach and "
                    "impression denominators are absent."
                ),
            ],
        ),
        (
            "03_exploratory_data_analysis.ipynb",
            "Exploratory Data Analysis",
            "Compare post type, time, and engagement using the cleaned dataset.",
            [
                nbformat.v4.new_code_cell(
                    "import pandas as pd\n"
                    "from src.config import PROCESSED_CSV\n"
                    "frame = pd.read_csv(PROCESSED_CSV, parse_dates=['status_published'])\n"
                    "by_type = frame.groupby('status_type')[['num_reactions','num_comments',"
                    "'num_shares','total_engagement']].agg(['count','mean','median']).round(2)\n"
                    "display(by_type)"
                ),
                nbformat.v4.new_code_cell(
                    "display(frame[['num_reactions','num_comments','num_shares',"
                    "'total_engagement']].corr(method='spearman').round(3))\n"
                    "display(frame.nlargest(10, 'total_engagement')[['status_id','status_type',"
                    "'status_published','total_engagement']])"
                ),
                nbformat.v4.new_code_cell(
                    "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'engagement_by_post_type.png')))\n"
                    "display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'engagement_correlation.png')))"
                ),
                nbformat.v4.new_markdown_cell(
                    "Means and medians are reported together because engagement is "
                    "strongly right-skewed. Correlations describe monotonic association "
                    "and are not interpreted as causal effects."
                ),
            ],
        ),
        (
            "04_network_analysis.ipynb",
            "Network Analysis",
            "Recreate supplied graph definitions and inspect structural metrics.",
            [
                nbformat.v4.new_code_cell(
                    "from src.graph_generators import build_transport_graph, build_ppi_graph, graph_metrics\n"
                    "graphs = {'G_transport': build_transport_graph(), 'G_ppi': build_ppi_graph()}\n"
                    "for name, graph in graphs.items():\n"
                    "    print(name)\n"
                    "    display(graph_metrics(graph))"
                ),
                nbformat.v4.new_code_cell(
                    "import pandas as pd\n"
                    "display(pd.read_csv(ROOT / 'outputs' / 'tables' / 'generative_models_comparison.csv'))\n"
                    "display(pd.read_csv(ROOT / 'outputs' / 'tables' / 'domain_graph_metrics.csv').head())"
                ),
                nbformat.v4.new_markdown_cell(
                    "The Facebook table remains outside the relationship-graph analysis "
                    "because it has no verified relational identifiers. All relationship "
                    "graphs in the exercises are explicitly synthetic."
                ),
            ],
        ),
        (
            "05_interactive_visualization.ipynb",
            "Interactive Visualization",
            "Inspect and verify the standalone Plotly deliverables.",
            [
                nbformat.v4.new_code_cell(
                    "from src.config import INTERACTIVE\n"
                    "files = sorted(INTERACTIVE.glob('*.html'))\n"
                    "for path in files:\n"
                    "    text = path.read_text(encoding='utf-8')\n"
                    "    print(path.name, f'{path.stat().st_size/1024:.1f} KiB', "
                    "'absolute local path=' + str('file:///' in text or str(ROOT) in text))"
                ),
                nbformat.v4.new_code_cell(
                    "social_html = (INTERACTIVE / 'network_color_toggle_dashboard.html').read_text(encoding='utf-8')\n"
                    "assert 'Color by Interest Group' in social_html\n"
                    "assert 'Color by In-Degree' in social_html\n"
                    "assert 'updatemenus' in social_html\n"
                    "print('Dropdown contract verified.')"
                ),
                nbformat.v4.new_markdown_cell(
                    "Standalone HTML permits zooming, panning, hover inspection, and "
                    "responsive embedding without a Python server. Final interaction "
                    "behavior is additionally checked in a browser."
                ),
            ],
        ),
        (
            "06_hands_on_network_exercises.ipynb",
            "Hands-On Network Visualization Exercises",
            "Reproduce and interpret all seven mandatory exercises.",
            _exercise_cells(),
        ),
    ]

    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, title, purpose, extra_cells in specs:
        notebook = nbformat.v4.new_notebook()
        notebook["metadata"]["kernelspec"] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        notebook["metadata"]["language_info"] = {
            "name": "python",
            "version": f"{sys.version_info.major}.{sys.version_info.minor}",
        }
        notebook["cells"] = [*_base_cells(title, purpose), *extra_cells]
        stem = Path(filename).stem.replace("_", "-")
        for index, cell in enumerate(notebook["cells"], start=1):
            cell["id"] = f"{stem[:48]}-{index:02d}"
        path = NOTEBOOKS / filename
        nbformat.write(notebook, path)
        written.append(path)
    return written


def execute_notebooks(paths: list[Path] | None = None) -> list[Path]:
    """Execute notebooks from a clean kernel and save their outputs in place."""

    selected = paths or sorted(NOTEBOOKS.glob("*.ipynb"))
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{original_path}"
    try:
        for path in selected:
            notebook = nbformat.read(path, as_version=4)
            client = NotebookClient(
                notebook,
                timeout=600,
                kernel_name="python3",
                resources={"metadata": {"path": str(ROOT)}},
                allow_errors=False,
                record_timing=False,
            )
            client.execute(cwd=str(ROOT))
            nbformat.write(notebook, path)
    finally:
        os.environ["PATH"] = original_path
    return selected
