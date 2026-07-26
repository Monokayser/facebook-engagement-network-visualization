# Visual Analytics and Network Analysis of Facebook Engagement Using Python

A reproducible academic project that analyzes 7,050 anonymized Facebook posts and completes seven graph-visualization exercises with Python, Pandas, NetworkX, Matplotlib, NumPy, SciPy, and Plotly.

**Public website:** [GitHub Pages](https://monokayser.github.io/facebook-engagement-network-visualization/)
**Source repository:** [Monokayser/facebook-engagement-network-visualization](https://github.com/Monokayser/facebook-engagement-network-visualization)

**Student:** S. M. Monowar Kayser (`253-25-019`)  
**Course:** Data Visualization (`CSE628`), Summer 2026  
**Teacher:** Sadat Hasan, Adjunct Faculty  
**Department:** Department of Computer Science and Engineering  
**University:** Daffodil International University

## Project overview

The project has two deliberately separated analytical scopes:

- **Empirical Facebook analysis:** post-level reactions, comments, shares, content type, and publishing time.
- **Synthetic network exercises:** graph representations, six layouts, bipartite enrollment, weighted Barabási-Albert encoding, model comparison, an interactive directed social network, and an applied-AI research knowledge graph.

The Facebook source table does not contain verified user-to-user relationships. The project therefore does not invent them.

## Dataset

| Field | Value |
|---|---|
| Title | Facebook Live Sellers in Thailand |
| Author | Nassim Dehouche |
| Publisher | UCI Machine Learning Repository |
| DOI | [10.24432/C5R60S](https://doi.org/10.24432/C5R60S) |
| Official source | [UCI dataset page](https://archive.ics.uci.edu/dataset/488/facebook%2Blive%2Bsellers%2Bin%2Bthailand) |
| Kaggle mirror | [Facebook Live Sellers in Thailand, UCI ML Repo](https://www.kaggle.com/datasets/ashishg21/facebook-live-sellers-in-thailand-uci-ml-repo) |
| License | Creative Commons Attribution 4.0 International |
| Raw dimensions | 7,050 rows × 16 columns |
| Processed dimensions | 7,050 rows × 27 columns |
| Format | CSV |
| Download date | 2026-07-25 |

The official UCI archive was used because Kaggle API credentials were not configured. The project does not claim Kaggle API use.

## Research objectives

1. Build an auditable cleaning and feature-engineering workflow.
2. Compare reactions, comments, shares, and total engagement across post types and time.
3. Complete all seven exercises using the supplied teaching graph definitions.
4. Compare static and interactive network encodings.
5. Generate consistent tables, figures, notebooks, reports, tests, and a responsive website from one pipeline.

## Key findings

- The table records 1,622,326 reactions, 1,581,710 comments, and 282,159 shares.
- Mean total engagement is 494.50, while the median is 69, confirming strong right skew.
- Videos have the highest observed mean total engagement (1,041.57); this is descriptive, not causal.
- The weighted `G_transport` matrix is symmetric.
- The supplied `G_ppi` realization has average clustering `0.000`; Kamada-Kawai best clarifies ring locality and shortcuts, but no layout can reveal triangle clusters that do not exist.
- Data Visualization is the most popular synthetic course (12 enrollments); Imran Kabir takes the most courses (5).
- Section 6's BA graph has 196 edges with seeded weights from 1 to 10.
- Watts-Strogatz captures clustering and short paths, while Barabási-Albert captures hubs and heterogeneous degree.
- Recommendation Systems is the strongest synthetic bridge by inverse-strength weighted betweenness (`0.5385`).

## Technology

- Python 3.12
- Pandas and NumPy
- NetworkX and SciPy
- Matplotlib and Plotly
- Jupyter/nbformat
- python-docx and ReportLab
- pytest, Ruff, and Black
- Next.js/Vinext static-compatible site for public deployment

## Repository structure

```text
data/                    Raw, processed, and synthetic CSV data
notebooks/               Six executable analysis notebooks
exercises/README.md      Exercise-by-exercise documentation
src/                     Reusable Python modules
visualizations/          Static PNG and standalone interactive HTML
outputs/                 Verified JSON, tables, and exercise summaries
report/                  Markdown, DOCX, and PDF academic reports
public/                  Deployment-ready reports, images, data, and HTML
app/                     Responsive academic dashboard
website/                 Generated multi-page GitHub Pages site
tests/                   Python and rendered-site tests
main.py                  Complete reproducible pipeline
.github/workflows/       Continuous validation and Pages deployment
```

## Environment setup

Python 3.11 or 3.12 is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Optional Kaggle configuration

Keep `kaggle.json` outside the repository and follow Kaggle's official API credential instructions. The file is ignored by Git. Kaggle is optional because the reproducible acquisition route uses the official UCI archive.

## Reproduce the project

1. Confirm `data/raw/Live_20210128.csv` exists, or download the official UCI archive as described in [data/README.md](data/README.md).
2. Run the complete pipeline. It regenerates the cleaned data, exercises,
   visualizations, executed notebooks, reports, both website targets, and the
   SHA-256 artifact manifest:

   ```bash
   python main.py
   ```

3. The pipeline executes and saves the notebooks in this order:

   1. `01_data_understanding.ipynb`
   2. `02_data_cleaning.ipynb`
   3. `03_exploratory_data_analysis.ipynb`
   4. `04_network_analysis.ipynb`
   5. `05_interactive_visualization.ipynb`
   6. `06_hands_on_network_exercises.ipynb`

4. Run validation:

   ```bash
   black --check .
   ruff check .
   pytest
   ```

5. Build the website:

   ```bash
   pnpm install
   pnpm build
   ```

## Hands-On Network Visualization Exercises

1. **Weighted adjacency representations** — [notebook](notebooks/06_hands_on_network_exercises.ipynb), [matrix](outputs/tables/g_transport_adjacency_matrix.csv), [report](report/report.md#81-exercise-1-weighted-adjacency-representations)
2. **Six-layout comparison** — [figure](visualizations/static/g_ppi_layout_comparison.png), [report](report/report.md#82-exercise-2-network-layout-comparison)
3. **Student-course bipartite graph** — [figure](visualizations/static/student_course_bipartite_graph.png), [degree table](outputs/tables/student_course_degree_summary.csv)
4. **Weighted Barabási-Albert graph** — [figure](visualizations/static/barabasi_albert_weighted.png), [edge weights](outputs/tables/barabasi_albert_edge_weights.csv)
5. **Generative-model statistics** — [table](outputs/tables/generative_models_comparison.csv), [degree distributions](visualizations/static/generative_models_degree_distribution.png)
6. **Interactive node-color dashboard** — [standalone HTML](visualizations/interactive/network_color_toggle_dashboard.html)
7. **Applied AI and Multimedia graph** — [interactive HTML](visualizations/interactive/domain_graph.html), [metrics](outputs/tables/domain_graph_metrics.csv)

Use the [step-by-step exercise website](https://monokayser.github.io/facebook-engagement-network-visualization/exercises/)
to work through all seven studies in order. Detailed implementation notes and
limitations are in [exercises/README.md](exercises/README.md).

## Reports and dashboard

- [Academic report (Markdown)](report/report.md)
- [Academic report (DOCX)](report/report.docx)
- [Academic report (PDF)](report/report.pdf)
- [Verified analytical summary](outputs/analysis_summary.json)

The interactive dashboard embeds self-contained Plotly files, works without local absolute paths, and provides responsive desktop, tablet, and mobile layouts.

Every exercise has a dedicated generated web page containing its source
definition, relevant data download, Python implementation, visual output,
verified result, interpretation, limitation, report link, and direct links to
the canonical source modules. Previous/next controls preserve the intended
one-by-one learning sequence.

## Public deployment

GitHub Actions rebuilds the project with Python 3.12, validates the notebooks,
tests, reports, and site assets, and deploys `website/` through GitHub Pages.
Relative URLs make the static site safe under the repository subpath. The
configured Sites project is maintained as a secondary deployment of the same
canonical content.

## Testing

The test suite covers source loading, required columns, duplicate and missing-value handling, feature engineering, graph construction, bipartite validation, weight ranges, adjacency symmetry, disconnected path handling, static and interactive outputs, report generation, and path portability.

## Limitations and ethics

The data end in 2018 and represent ten Thai sellers. Reach, impressions, page identity, follower count, campaign spend, and content text are unavailable. Observed associations cannot establish causality or generalize automatically to other settings. The source is anonymized; this project preserves that protection and clearly labels synthetic data.

## License and acknowledgements

Project code and original documentation are released under the [MIT License](LICENSE). The dataset remains CC BY 4.0 and must be attributed to Nassim Dehouche and UCI. The supplied graph-teaching materials informed the exercise graph definitions but are not republished because their license was not stated.

Acknowledgements: Sadat Hasan, the Department of Computer Science and Engineering at Daffodil International University, the UCI Machine Learning Repository, and the maintainers of Pandas, NetworkX, Matplotlib, Plotly, NumPy, SciPy, Jupyter, pytest, and python-docx.
