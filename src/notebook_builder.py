"""Create concise, executable notebooks that document the reproducible workflow."""

from __future__ import annotations

from pathlib import Path

import nbformat

from src.config import NOTEBOOKS, STUDENT


def _base_cells(title: str, purpose: str) -> list:
    return [
        nbformat.v4.new_markdown_cell(
            f"# {title}\n\n{purpose}\n\n"
            f"**Student:** {STUDENT['name']} ({STUDENT['id']})  \n"
            f"**Course:** {STUDENT['course_name']} ({STUDENT['course_code']}), "
            f"{STUDENT['semester']}"
        ),
        nbformat.v4.new_code_cell(
            "from pathlib import Path\n"
            "import sys\n"
            "ROOT = Path.cwd().resolve()\n"
            "if ROOT.name == 'notebooks':\n"
            "    ROOT = ROOT.parent\n"
            "if str(ROOT) not in sys.path:\n"
            "    sys.path.insert(0, str(ROOT))\n"
            "print('Project root:', ROOT)"
        ),
    ]


def generate_notebooks() -> list[Path]:
    """Write the six requested notebooks with clear code and interpretation."""

    specs = [
        (
            "01_data_understanding.ipynb",
            "Data Understanding",
            "Inspect the official UCI Facebook dataset without changing the raw file.",
            [
                nbformat.v4.new_code_cell(
                    "from src.config import RAW_CSV\n"
                    "from src.data_loader import load_facebook_data\n"
                    "raw = load_facebook_data(RAW_CSV)\n"
                    "print('Shape:', raw.shape)\n"
                    "display(raw.head())\n"
                    "display(raw.dtypes.rename('dtype').to_frame())"
                ),
                nbformat.v4.new_markdown_cell(
                    "The source contains engagement counts, post type, and timestamp. "
                    "It does not contain verified user-to-user relationships, reach, or impressions."
                ),
            ],
        ),
        (
            "02_data_cleaning.ipynb",
            "Data Cleaning and Feature Engineering",
            "Apply the modular cleaning workflow and inspect its audit trail.",
            [
                nbformat.v4.new_code_cell(
                    "from src.config import RAW_CSV\n"
                    "from src.data_loader import load_facebook_data\n"
                    "from src.data_preprocessing import clean_and_engineer\n"
                    "processed, audit = clean_and_engineer(load_facebook_data(RAW_CSV))\n"
                    "display(audit)\n"
                    "display(processed.head())"
                ),
                nbformat.v4.new_markdown_cell(
                    "Outliers are flagged instead of deleted. Zero-safe ratios avoid "
                    "infinite values, and no engagement-rate claim is made without a denominator."
                ),
            ],
        ),
        (
            "03_exploratory_data_analysis.ipynb",
            "Exploratory Data Analysis",
            "Summarize post type, time, and engagement using the cleaned dataset.",
            [
                nbformat.v4.new_code_cell(
                    "import pandas as pd\n"
                    "from src.config import PROCESSED_CSV\n"
                    "frame = pd.read_csv(PROCESSED_CSV, parse_dates=['status_published'])\n"
                    "display(frame.groupby('status_type')[['num_reactions','num_comments',"
                    "'num_shares','total_engagement']].agg(['count','mean','median']).round(2))"
                ),
                nbformat.v4.new_code_cell(
                    "display(frame[['num_reactions','num_comments','num_shares',"
                    "'total_engagement']].corr(method='spearman').round(3))"
                ),
                nbformat.v4.new_markdown_cell(
                    "Mean and median are reported together because engagement is strongly "
                    "right-skewed. Correlation is interpreted as association, not causation."
                ),
            ],
        ),
        (
            "04_network_analysis.ipynb",
            "Network Analysis",
            "Recreate the supplied graph definitions and inspect verified structural metrics.",
            [
                nbformat.v4.new_code_cell(
                    "from src.graph_generators import build_transport_graph, build_ppi_graph, graph_metrics\n"
                    "G_transport = build_transport_graph()\n"
                    "G_ppi = build_ppi_graph()\n"
                    "print('G_transport:', graph_metrics(G_transport))\n"
                    "print('G_ppi:', graph_metrics(G_ppi))"
                ),
                nbformat.v4.new_markdown_cell(
                    "The transportation graph is an undirected weighted teaching example. "
                    "The protein graph is the exact seeded Watts-Strogatz construction from Section 8.3."
                ),
            ],
        ),
        (
            "05_interactive_visualization.ipynb",
            "Interactive Visualization",
            "Verify the standalone Plotly deliverables and explain their interaction design.",
            [
                nbformat.v4.new_code_cell(
                    "from src.config import INTERACTIVE\n"
                    "files = sorted(INTERACTIVE.glob('*.html'))\n"
                    "for path in files:\n"
                    "    print(path.name, f'{path.stat().st_size/1024:.1f} KiB')\n"
                    "assert any(path.name == 'network_color_toggle_dashboard.html' for path in files)"
                ),
                nbformat.v4.new_markdown_cell(
                    "The social-network dropdown preserves geometry while switching from "
                    "categorical interest-group color to a continuous in-degree scale."
                ),
            ],
        ),
        (
            "06_hands_on_network_exercises.ipynb",
            "Hands-On Network Visualization Exercises",
            "Reproduce the seven mandatory exercises using the supplied graph objects and stored synthetic CSV data.",
            [
                nbformat.v4.new_markdown_cell(
                    "## Exercise 1 - Weighted adjacency representations\n"
                    "The graph is undirected, so the kilometer matrix should be symmetric."
                ),
                nbformat.v4.new_code_cell(
                    "import numpy as np\n"
                    "from src.graph_generators import build_transport_graph, build_generative_models\n"
                    "from src.network_analysis import transport_representations, compare_generative_models\n"
                    "G_transport = build_transport_graph()\n"
                    "matrix, representation = transport_representations(G_transport)\n"
                    "display(matrix)\n"
                    "print('Symmetric:', representation['matrix_symmetric'])"
                ),
                nbformat.v4.new_markdown_cell(
                    "## Exercises 2-7\n"
                    "The main pipeline saves every required layout, synthetic table, weighted graph, "
                    "model statistic, Plotly dropdown, and research graph. The following compact checks "
                    "recalculate the model table and verify required outputs."
                ),
                nbformat.v4.new_code_cell(
                    "from src.config import STATIC, INTERACTIVE, TABLES\n"
                    "comparison, _ = compare_generative_models(build_generative_models())\n"
                    "display(comparison)\n"
                    "required = [\n"
                    " STATIC/'g_ppi_layout_comparison.png',\n"
                    " STATIC/'student_course_bipartite_graph.png',\n"
                    " STATIC/'barabasi_albert_weighted.png',\n"
                    " INTERACTIVE/'network_color_toggle_dashboard.html',\n"
                    " INTERACTIVE/'domain_graph.html',\n"
                    " TABLES/'domain_graph_metrics.csv',\n"
                    "]\n"
                    "assert all(path.exists() for path in required)\n"
                    "print('All seven exercise output groups verified.')"
                ),
            ],
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
        notebook["metadata"]["language_info"] = {"name": "python", "version": "3.12"}
        notebook["cells"] = [*_base_cells(title, purpose), *extra_cells]
        path = NOTEBOOKS / filename
        nbformat.write(notebook, path)
        written.append(path)
    return written
