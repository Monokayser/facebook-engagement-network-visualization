# Hands-On Network Visualization Exercises

All stochastic operations use seed `42`. Exercise definitions reuse the supplied teaching notebook wherever a source graph exists.

## Exercise 1 — Weighted adjacency representations

- **Objective:** Reuse Section 8.2 `G_transport`; print its adjacency list and create the kilometer matrix.
- **Libraries:** NetworkX, Pandas, NumPy.
- **Outputs:** `outputs/tables/g_transport_adjacency_matrix.csv`, `outputs/exercise_01_summary.txt`.
- **Result:** The matrix is symmetric because the graph is undirected and each route has one shared weight.
- **Limitation:** The seven-city graph is a teaching example, not a complete route system.
- **Report:** Section 8.1.

## Exercise 2 — Six-layout comparison

- **Objective:** Draw Section 8.3 `G_ppi` with spring, circular, shell, spectral, Kamada-Kawai, and random layouts.
- **Libraries:** NetworkX, Matplotlib, SciPy.
- **Outputs:** One comparison PNG and six individual 300-DPI PNG files.
- **Result:** Kamada-Kawai best reveals ring locality and rewired shortcuts for this realization.
- **Limitation:** The measured average clustering coefficient is `0.000`; no layout can reveal triangle clusters that are absent from the source graph.
- **Report:** Section 8.2.

## Exercise 3 — Student-course bipartite graph

- **Objective:** Build enrollment from stored synthetic CSV tables.
- **Libraries:** Pandas, NetworkX, Matplotlib.
- **Outputs:** Three CSV inputs, the graph PNG, and a degree summary table.
- **Result:** Data Visualization has 12 enrollments; Imran Kabir takes 5 courses.
- **Limitation:** Synthetic data do not describe real DIU enrollment.
- **Report:** Section 8.3.

## Exercise 4 — Weighted Barabási-Albert graph

- **Objective:** Add reproducible integer weights from 1 to 10 to Section 6's 100-node BA graph.
- **Libraries:** NetworkX, Matplotlib, Pandas.
- **Outputs:** Unweighted and weighted PNG files and a 196-row edge-weight table.
- **Result:** Width makes selected ties visually salient but does not automatically change degree centrality.
- **Limitation:** Random weights demonstrate encoding only.
- **Report:** Section 8.4.

## Exercise 5 — Generative-model statistics

- **Objective:** Compare the exact Section 3 Erdős-Rényi, Watts-Strogatz, and Barabási-Albert models.
- **Libraries:** NetworkX, NumPy, Pandas, Matplotlib.
- **Outputs:** Statistical comparison CSV and four degree-distribution PNG files.
- **Result:** Watts-Strogatz captures clustering and short paths; Barabási-Albert captures hubs and heterogeneous degree.
- **Limitation:** One 30-node seeded realization per model is parameter-sensitive.
- **Report:** Section 8.5.

## Exercise 6 — Interactive Plotly dashboard

- **Objective:** Extend Section 9's directed graph with a node-color dropdown.
- **Libraries:** NetworkX, Plotly.
- **Outputs:** `visualizations/interactive/network_color_toggle_dashboard.html` and its website copy.
- **Result:** Interest-group and in-degree color modes preserve positions and visible edges.
- **Limitation:** Plotly line segments do not display arrowheads; direction is available through in/out-degree values.
- **Report:** Section 8.6.

## Exercise 7 — Applied AI and Multimedia research graph

- **Objective:** Build a typed, weighted synthetic knowledge graph from CSV files.
- **Libraries:** Pandas, NetworkX, Matplotlib, Plotly.
- **Outputs:** Node and edge CSV files, a static PNG, an interactive HTML file, and a centrality table.
- **Result:** Recommendation Systems has the highest weighted betweenness (`0.3663`).
- **Limitation:** The graph is illustrative and is not extracted from publications.
- **Report:** Section 8.7.

## Notebook

Run `notebooks/06_hands_on_network_exercises.ipynb` after `python main.py` to recalculate the principal checks and inspect the generated table.
