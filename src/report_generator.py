"""Generate the academic Markdown, DOCX, and PDF reports from verified results."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.config import ANALYSIS_SUMMARY, REPORT, STATIC, STUDENT

NAVY = RGBColor(23, 50, 77)
BLUE = RGBColor(57, 115, 168)
GRAY = RGBColor(82, 96, 109)
LIGHT = "E9EEF3"


def _fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def _load_summary(path: Path = ANALYSIS_SUMMARY) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def build_markdown(summary: dict[str, Any]) -> str:
    """Create a complete academic report in Markdown from calculated results."""

    engagement = summary["engagement"]
    audit = summary["data_cleaning"]
    transport = summary["exercises"]["exercise_1"]
    bipartite = summary["exercises"]["exercise_3"]
    weighted = summary["exercises"]["exercise_4"]
    models = summary["exercises"]["exercise_5"]
    domain = summary["exercises"]["exercise_7"]
    type_rows = "\n".join(
        (
            f"| {row['status_type'].title()} | {row['posts']:,} | "
            f"{row['mean_reactions']:,.2f} | {row['mean_comments']:,.2f} | "
            f"{row['mean_shares']:,.2f} | {row['mean_total_engagement']:,.2f} |"
        )
        for row in engagement["by_type"]
    )
    model_rows = "\n".join(
        (
            f"| {row['Model']} | {row['Nodes']} | {row['Edges']} | "
            f"{row['Density']:.3f} | {row['Average Clustering']:.3f} | "
            f"{row['Average Shortest Path']:.3f} ({row['Path Length Scope']}) | "
            f"{row['Maximum Degree']} | {row['Degree Standard Deviation']:.3f} |"
        )
        for row in models["records"]
    )
    return f"""# Visual Analytics and Network Analysis of Facebook Engagement Using Python

**Student:** {STUDENT['name']}  
**Student ID:** {STUDENT['id']}  
**Course:** {STUDENT['course_name']} ({STUDENT['course_code']})  
**Semester:** {STUDENT['semester']}  
**Teacher:** {STUDENT['teacher']}, {STUDENT['designation']}  
**Department:** {STUDENT['department']}  
**University:** {STUDENT['university']}

## Abstract

This project analyzes {engagement['rows']:,} anonymized Facebook posts from ten Thai fashion and cosmetics sellers and extends the supplied graph-visualization teaching material through seven reproducible exercises. The analysis combines data cleaning, feature engineering, exploratory visualization, graph representations, layout comparison, bipartite modeling, weighted encoding, generative-model statistics, and interactive Plotly networks. The dataset records {engagement['total_reactions']:,} reactions, {engagement['total_comments']:,} comments, and {engagement['total_shares']:,} shares. {engagement['top_post_type_by_mean_engagement'].title()} posts have the largest mean total engagement ({engagement['top_post_type_mean_engagement']:,.2f}), although the observational design does not support a causal claim. The weighted `G_transport` adjacency matrix is symmetric, while the model comparison shows a trade-off: Watts-Strogatz captures clustering and short paths, whereas Barabasi-Albert captures hubs and degree heterogeneity. The result is a reproducible academic artifact with static figures, interactive HTML, executable notebooks, a responsive website, automated tests, and machine-readable analytical outputs.

**Keywords:** Facebook engagement, data visualization, social-network analysis, NetworkX, Plotly, graph layout, Python

## 1. Introduction

Social-media engagement is multidimensional: lightweight reactions coexist with comments and shares that may require greater effort. A responsible visual analysis must therefore preserve individual measures while also making aggregate patterns legible. This study addresses two linked tasks. First, it describes post-level engagement in an anonymized, publicly licensed Facebook dataset. Second, it applies and extends the graph concepts in the supplied course notebook so that representations, layouts, weights, centrality, and interaction can be compared using reproducible evidence.

### 1.1 Problem statement

Raw engagement counts are highly skewed, post categories are imbalanced, and a tabular engagement dataset does not contain verified user-to-user relationships. Treating rows as a social network would invent edges. The project therefore keeps the empirical Facebook analysis tabular and labels the assignment's relationship graphs as synthetic.

### 1.2 Objectives

1. Construct a reproducible cleaning and feature-engineering workflow.
2. Describe engagement differences across post type and time without causal overreach.
3. Complete all seven mandatory graph exercises using the supplied graph definitions.
4. Compare static and interactive visual encodings.
5. publish auditable outputs through documentation, tests, a report, and a responsive dashboard.

### 1.3 Research questions

1. How do reactions, comments, shares, and total engagement vary across post types?
2. Which temporal patterns are visible in posting activity and median engagement?
3. How do graph layout and edge-weight encodings change structural interpretation?
4. Which canonical generative model reproduces particular social-network properties?
5. Which nodes occupy structurally important positions in the synthetic research graph?

## 2. Dataset and provenance

The dataset is **Facebook Live Sellers in Thailand**, authored by Nassim Dehouche and distributed by the UCI Machine Learning Repository under CC BY 4.0 [1]. The raw CSV contains 7,050 rows and 16 columns; four columns are entirely empty placeholders. Posts span {engagement['date_min'][:10]} through {engagement['date_max'][:10]}. The official UCI file was used because Kaggle credentials were not configured; a Kaggle mirror is documented but was not used for acquisition. The original study reports anonymized data collected from ten Thai fashion and cosmetics seller pages [2].

The selection is appropriate because it is medium-sized, includes numerical and categorical engagement variables, contains timestamps, is publicly licensed, and contains no names or message text. Its limitation is equally important: it does not contain reach, impressions, follower counts, page identity, or user-to-user interaction IDs.

## 3. Tools and reproducibility

Python is the primary language. Pandas performs data preparation, NumPy supports numerical operations, NetworkX constructs and measures graphs, Matplotlib creates 300-DPI static figures, Plotly produces standalone interactive HTML, SciPy supports NetworkX's Kamada-Kawai layout path, python-docx creates the editable report, ReportLab provides a PDF fallback, nbformat creates notebooks, and pytest validates the workflow. Fixed seed 42 controls every stochastic graph and layout where the API accepts a seed.

## 4. Data-cleaning methodology

The raw file was preserved unchanged. Column names were standardized; {len(audit['empty_columns_removed'])} entirely empty columns were removed; numeric engagement fields were coerced, checked for nonnegative values, and stored as integers; timestamps were parsed; categories were normalized; and duplicates were checked by full row and `status_id`. The pipeline removed {audit['duplicate_rows_removed']} duplicate rows and {audit['duplicate_ids_removed']} duplicate IDs. It removed {audit['invalid_dates_removed']} invalid timestamps and imputed {audit['numeric_missing_values_imputed']} missing numeric values. The final analytical table contains {audit['final_rows']:,} rows and {audit['final_columns']} columns.

Outliers are flagged, not deleted, using the upper Tukey fence on total engagement ({audit['outlier_threshold']:,.2f}); {audit['outlier_count']:,} posts exceed the threshold. This preserves genuine high-performing posts while making skew explicit.

## 5. Feature engineering

- **Total engagement** = reactions + comments + shares.
- **Like-to-comment ratio** = likes / comments, with zero returned when comments are zero.
- **Share-to-engagement ratio** = shares / total engagement, with zero-safe division.
- **Positive reaction percentage** = (likes + loves + wows) / sum of recorded reaction components × 100.
- **Negative reaction percentage** = (sads + angrys) / sum of recorded reaction components × 100.
- **Temporal features** include posting hour, weekday, month, ISO week, weekend flag, and time-of-day band.
- **Engagement category** assigns low, medium, and high groups by rank-based tertiles.

No engagement-rate feature is claimed because reach or impressions are absent.

## 6. Exploratory data analysis

The dataset contains {engagement['post_type_counts']['photo']:,} photos, {engagement['post_type_counts']['video']:,} videos, {engagement['post_type_counts']['status']:,} status posts, and {engagement['post_type_counts']['link']:,} links. Total engagement is {engagement['total_engagement']:,}; its mean is {engagement['mean_engagement']:,.2f} and median is {engagement['median_engagement']:,.2f}, demonstrating right skew. The hour with the largest observed median engagement is {engagement['best_median_posting_hour']:02d}:00 ({engagement['best_median_posting_hour_value']:,.2f}), but this association may reflect content mix, seller behavior, seasonality, or other unobserved factors.

**Table 1. Engagement summary by post type**

| Post type | Posts | Mean reactions | Mean comments | Mean shares | Mean total engagement |
|---|---:|---:|---:|---:|---:|
{type_rows}

![Mean engagement components by post type](../visualizations/static/engagement_by_post_type.png)

*Figure 1. Mean reactions, comments, and shares by post type.*

![Engagement distributions](../visualizations/static/engagement_distribution.png)

*Figure 2. Log-transformed total-engagement distributions reveal substantial right skew.*

![Correlation heatmap](../visualizations/static/engagement_correlation.png)

*Figure 3. Spearman correlations describe monotonic association rather than causation.*

## 7. Graph representation and visualization methodology

An adjacency matrix offers exact pairwise lookup, while a node-link diagram emphasizes paths, clusters, bridges, and hubs. Force-directed layouts encode graph topology into geometric proximity; circular and random layouts mainly impose placement rules unrelated to community quality. Node size, color, and edge width are kept semantically consistent within each comparison to isolate the effect of layout.

## 8. Mandatory hands-on network exercises

### 8.1 Exercise 1: Weighted adjacency representations

**Objective.** Reuse Section 8.2's seven-city `G_transport` graph and verify its weighted matrix.

**Method and implementation.** `nx.to_pandas_adjacency(..., weight="weight")` generated a labeled matrix, and `numpy.allclose(A, A.T)` tested symmetry.

**Result.** The matrix is symmetric: **{transport['matrix_symmetric']}**. Dhaka has six incident routes and therefore occupies the main hub row and column. The matrix stores kilometer values, not binary indicators.

**Interpretation.** An undirected edge contributes the same weight to `(u,v)` and `(v,u)`. The matrix would not need to be symmetric for a directed graph or when directional weights differ.

**Limitation.** The transportation graph is a teaching example rather than a complete national route network.

### 8.2 Exercise 2: Network layout comparison

**Objective.** Draw `G_ppi` with spring, circular, shell, spectral, Kamada-Kawai, and random layouts while holding visual encoding constant.

**Result and interpretation.** The **Kamada-Kawai layout** is selected as the clearest view for this small graph. It minimizes graph-theoretic distance stress across all node pairs and makes the ring-like locality plus rewired shortcuts more legible than circular, shell, spectral, or random placement. Spring is a close alternative. Crucially, the supplied `k=3` realization has a measured average clustering coefficient of {summary['exercises']['exercise_2']['average_clustering']:.3f}. No layout can reveal triangle-based clustering that is absent; the selected layout therefore clarifies distance structure and shortcuts, not empirical communities. The conclusion is layout-specific rather than a claim that one algorithm is universally superior.

![Six-layout comparison](../visualizations/static/g_ppi_layout_comparison.png)

*Figure 4. Six layouts of the identical `G_ppi` graph.*

**Limitation.** Visual cluster separation is not itself a community-detection result.

### 8.3 Exercise 3: Student-course bipartite network

**Objective.** Model synthetic enrollment between {bipartite['students']} students and {bipartite['courses']} courses from stored CSV tables.

**Result.** NetworkX confirms bipartiteness. The graph has {bipartite['enrollments']} enrollments. **{bipartite['most_popular_course']}** is most popular ({bipartite['most_popular_course_enrollments']} enrollments), and **{bipartite['most_enrolled_student']}** takes the most courses ({bipartite['most_enrolled_student_courses']}).

![Student-course graph](../visualizations/static/student_course_bipartite_graph.png)

*Figure 5. Synthetic enrollment graph; circles are students and squares are courses.*

**Interpretation.** {bipartite['pattern']}

**Limitation.** The graph is synthetic and cannot support conclusions about actual DIU enrollment.

### 8.4 Exercise 4: Weighted Barabasi-Albert visualization

**Objective.** Extend Section 6's 100-node BA graph with seeded integer edge weights from 1 through 10.

**Result.** {weighted['edges']} edges received weights with observed range {weighted['minimum_weight']}–{weighted['maximum_weight']} and mean {weighted['mean_weight']:.2f}. Width makes high-weight ties salient, but hubs remain defined by node degree rather than edge width.

![Weighted BA graph](../visualizations/static/barabasi_albert_weighted.png)

*Figure 6. Synthetic BA graph with normalized edge-width encoding.*

**Interpretation.** The view changes which ties attract attention, but random exercise weights do not constitute empirical importance. Edge weight and node centrality can interact, yet they are not interchangeable.

**Limitation.** Random weights demonstrate encoding only.

### 8.5 Exercise 5: Statistical comparison of generative models

**Table 2. Statistical comparison of Section 3 models**

| Model | Nodes | Edges | Density | Avg. clustering | Avg. path | Max degree | Degree SD |
|---|---:|---:|---:|---:|---:|---:|---:|
{model_rows}

![Generative-model degree distributions](../visualizations/static/generative_models_degree_distribution.png)

*Figure 7. Degree distributions expose homogeneous, small-world, and hub-dominated structures.*

**Interpretation.** Watts-Strogatz best captures high clustering with short paths, whereas Barabasi-Albert best captures hubs and heterogeneous degree. A realistic social network may combine both properties; none of these simple models is universally best. Erdős-Rényi provides a useful random baseline but lacks both mechanisms.

**Limitation.** Results come from one seeded 30-node realization per model and are sensitive to parameter choice.

### 8.6 Exercise 6: Interactive node-color dashboard

The standalone Plotly dashboard preserves node positions while a dropdown toggles between categorical interest-group color and continuous in-degree color. Hover text reports node ID, group, in-degree, and out-degree. Edges remain visible in both modes. The synthetic graph reuses the supplied Section 9 generation logic and is embedded in the final website.

**Limitation.** Directed edges are represented as line segments without arrowheads in Plotly; direction remains available through in/out-degree metrics and the graph definition.

### 8.7 Exercise 7: Research-domain network

**Objective.** Represent a synthetic knowledge graph for Applied AI and Multimedia using 15 typed nodes and 21 weighted semantic links.

**Result.** **{domain['top_betweenness_node']}** has the highest weighted betweenness ({domain['top_betweenness_value']:.4f}).

![Research-domain graph](../visualizations/static/domain_graph.png)

*Figure 8. Synthetic applied-AI and multimedia research knowledge graph.*

**Interpretation.** {domain['interpretation']}

**Limitation.** Nodes and relationships are illustrative and not extracted from publications.

## 9. Discussion

The empirical and synthetic components answer different questions. The Facebook table supports descriptive comparison of observed posts; it does not reveal individual users, verified follower ties, or causal effects. The synthetic graphs instead demonstrate how topology, representation, layout, and visual encoding affect interpretation. Keeping these scopes separate prevents a common analytical error: inferring social relationships that the source data never recorded.

The engagement analysis shows a mixture of high-frequency photos and high-engagement videos. Mean comparisons are influenced by extreme posts, so medians, log distributions, and Tukey flags accompany them. Rank correlations are preferable to a sole reliance on Pearson correlation under strong skew, but they still describe association only.

## 10. Limitations and ethical considerations

The data end in 2018, cover ten sellers in Thailand, and may not generalize to other countries, sectors, platforms, or current Facebook behavior. Page identity and content text are absent, reducing both explanatory power and privacy risk. Platform algorithms, audience size, campaign spend, and post quality are unobserved confounders. The analysis avoids re-identification, preserves anonymization, reports only aggregated results, and distinguishes real observations from synthetic exercises.

## 11. Conclusion and recommendations

This project demonstrates a reproducible bridge between tabular engagement analytics and network visualization. Video posts show the highest observed mean engagement, but the finding is descriptive. Kamada-Kawai most clearly presents the supplied small-world teaching graph, the weighted BA exercise distinguishes tie salience from node centrality, and the generative-model comparison shows why social-network realism is multidimensional.

Recommended next steps are to: (1) obtain ethically collected reach and impression denominators; (2) analyze multiple pages and time periods; (3) use repeated simulations and uncertainty intervals when comparing graph models; (4) test community detection separately from visual layout; and (5) retain the distinction between observed edges and synthetic teaching structures.

## 12. Future work

Future work could incorporate content embeddings, causal designs, hierarchical models for seller-level heterogeneity, temporal network models when genuine relational identifiers exist, and accessibility evaluation with classroom users.

## References

1. Dehouche, N. (2018). *Facebook Live Sellers in Thailand* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R60S
2. Dehouche, N. (2020). Dataset on usage and engagement patterns for Facebook Live sellers in Thailand. *Data in Brief, 30*, 105661. https://doi.org/10.1016/j.dib.2020.105661
3. Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. *Proceedings of SciPy 2008*, 11–15.
4. Barabasi, A.-L. (2016). *Network Science*. Cambridge University Press. http://networksciencebook.com/
5. Pandas documentation. https://pandas.pydata.org/docs/
6. Matplotlib documentation. https://matplotlib.org/stable/
7. Plotly Python documentation. https://plotly.com/python/
8. NetworkX documentation. https://networkx.org/documentation/stable/

## Appendix A. Reproducibility and output map

Run `python main.py` to rebuild processed data, analytical tables, figures, interactive HTML, notebooks, summary JSON, and reports. Run `pytest` for automated validation. The raw CSV remains in `data/raw/`, the cleaned table in `data/processed/`, required exercise tables in `outputs/tables/`, figures in `visualizations/`, and interactive artifacts in both `visualizations/interactive/` and the deployed website.

## Appendix B. Assumptions

The supplied teaching notebooks contain source-identical graph definitions. Exercise 2 uses Kamada-Kawai as the preferred layout based on this exact realization. The Kaggle API was not used. `num_reactions` is treated as the dataset's authoritative reaction total while component sums are retained as a quality-control comparison.
"""


def _set_cell_shading(cell, fill: str) -> None:
    properties = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def _set_repeat_table_header(row) -> None:
    properties = row._tr.get_or_add_trPr()
    table_header = OxmlElement("w:tblHeader")
    table_header.set(qn("w:val"), "true")
    properties.append(table_header)


def _add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Page ")
    run.font.name = "Calibri"
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, text, end])


def _configure_document(document: Document) -> None:
    """Apply the standard_business_brief preset with an editorial cover."""

    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)
    normal = document.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.1
    for style_name, size, before, after, color in (
        ("Title", 30, 0, 8, NAVY),
        ("Subtitle", 15, 0, 8, GRAY),
        ("Heading 1", 16, 16, 8, BLUE),
        ("Heading 2", 13, 12, 6, BLUE),
        ("Heading 3", 12, 8, 4, NAVY),
    ):
        style = document.styles[style_name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.color.rgb = color
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    header = section.header.paragraphs[0]
    header.text = "CSE628 | Facebook Engagement and Network Visualization"
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in header.runs:
        run.font.size = Pt(8.5)
        run.font.color.rgb = GRAY
    _add_page_number(section.footer.paragraphs[0])


def _add_figure(
    document: Document,
    path: Path,
    number: int,
    caption: str,
    alt_text: str,
) -> None:
    if not path.exists():
        return
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    shape = run.add_picture(str(path), width=Inches(6.15))
    doc_properties = shape._inline.docPr
    doc_properties.set("descr", alt_text)
    caption_paragraph = document.add_paragraph(style="Caption")
    caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_run = caption_paragraph.add_run(f"Figure {number}. {caption}")
    caption_run.italic = True
    caption_run.font.size = Pt(9)
    caption_paragraph.paragraph_format.keep_with_next = False


def _add_table(
    document: Document,
    title: str,
    headers: list[str],
    rows: Iterable[Iterable[Any]],
    widths: list[float] | None = None,
) -> None:
    title_paragraph = document.add_paragraph()
    title_run = title_paragraph.add_run(title)
    title_run.bold = True
    title_run.font.size = Pt(9.5)
    title_paragraph.paragraph_format.space_before = Pt(4)
    title_paragraph.paragraph_format.space_after = Pt(4)
    table = document.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.style = "Table Grid"
    header_row = table.rows[0]
    _set_repeat_table_header(header_row)
    for index, header in enumerate(headers):
        cell = header_row.cells[index]
        cell.text = header
        _set_cell_shading(cell, LIGHT)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(8.5)
    for values in rows:
        row = table.add_row()
        for index, value in enumerate(values):
            cell = row.cells[index]
            cell.text = str(value)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                for run in paragraph.runs:
                    run.font.size = Pt(8)
    if widths:
        for row in table.rows:
            for index, width in enumerate(widths):
                row.cells[index].width = Inches(width)


def build_docx(summary: dict[str, Any], path: Path) -> None:
    """Create the editable academic report with embedded tables and figures."""

    document = Document()
    _configure_document(document)
    document.add_paragraph("ACADEMIC PROJECT REPORT", style=None).alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )
    document.add_paragraph(
        "Visual Analytics and Network Analysis of Facebook Engagement Using Python",
        style="Title",
    ).alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph(
        "An empirical engagement study and seven reproducible network-visualization exercises",
        style="Subtitle",
    ).alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("\n")
    metadata = [
        ("Student", STUDENT["name"]),
        ("Student ID", STUDENT["id"]),
        ("Course", f"{STUDENT['course_name']} ({STUDENT['course_code']})"),
        ("Semester", STUDENT["semester"]),
        ("Teacher", f"{STUDENT['teacher']}, {STUDENT['designation']}"),
        ("Department", STUDENT["department"]),
        ("University", STUDENT["university"]),
    ]
    _add_table(
        document,
        "Submission details",
        ["Field", "Information"],
        metadata,
        widths=[1.55, 4.95],
    )
    document.add_paragraph("\nPrepared: 25 July 2026").alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )
    document.add_page_break()

    # Structured DOCX content mirrors the Markdown but uses Word-native form factors.
    sections = _docx_sections(summary)
    figure_number = 1
    for title, paragraphs, table_spec, figure_spec in sections:
        document.add_heading(title, level=1 if title[0].isdigit() else 2)
        for paragraph_text in paragraphs:
            paragraph = document.add_paragraph(paragraph_text)
            paragraph.paragraph_format.widow_control = True
        if table_spec:
            _add_table(document, **table_spec)
        if figure_spec:
            _add_figure(
                document,
                figure_spec[0],
                figure_number,
                figure_spec[1],
                figure_spec[2],
            )
            figure_number += 1
    document.add_page_break()
    document.add_heading("References", level=1)
    references = [
        "Dehouche, N. (2018). Facebook Live Sellers in Thailand [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R60S",
        "Dehouche, N. (2020). Dataset on usage and engagement patterns for Facebook Live sellers in Thailand. Data in Brief, 30, 105661. https://doi.org/10.1016/j.dib.2020.105661",
        "Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. Proceedings of SciPy 2008, 11-15.",
        "Barabasi, A.-L. (2016). Network Science. Cambridge University Press. http://networksciencebook.com/",
        "Pandas documentation. https://pandas.pydata.org/docs/",
        "Matplotlib documentation. https://matplotlib.org/stable/",
        "Plotly Python documentation. https://plotly.com/python/",
        "NetworkX documentation. https://networkx.org/documentation/stable/",
    ]
    for index, reference in enumerate(references, 1):
        document.add_paragraph(f"{index}. {reference}")
    document.add_heading("Appendix: Reproducibility and assumptions", level=1)
    document.add_paragraph(
        "Run python main.py to rebuild every generated artifact and pytest to validate "
        "the pipeline. The supplied teaching notebooks are source-identical. The "
        "official UCI download was used because Kaggle credentials were unavailable. "
        "All assignment-only relationship graphs are labeled synthetic."
    )
    document.core_properties.title = (
        "Visual Analytics and Network Analysis of Facebook Engagement Using Python"
    )
    document.core_properties.author = STUDENT["name"]
    document.core_properties.subject = f"{STUDENT['course_code']} academic project"
    document.save(path)


def _docx_sections(
    summary: dict[str, Any],
) -> list[tuple[str, list[str], dict[str, Any] | None, tuple[Path, str, str] | None]]:
    engagement = summary["engagement"]
    audit = summary["data_cleaning"]
    exercises = summary["exercises"]
    model_records = exercises["exercise_5"]["records"]
    type_rows = [
        [
            row["status_type"].title(),
            f"{row['posts']:,}",
            f"{row['mean_reactions']:,.2f}",
            f"{row['mean_comments']:,.2f}",
            f"{row['mean_shares']:,.2f}",
            f"{row['mean_total_engagement']:,.2f}",
        ]
        for row in engagement["by_type"]
    ]
    model_rows = [
        [
            row["Model"],
            row["Nodes"],
            row["Edges"],
            f"{row['Density']:.3f}",
            f"{row['Average Clustering']:.3f}",
            f"{row['Average Shortest Path']:.3f}",
            row["Maximum Degree"],
        ]
        for row in model_records
    ]
    return [
        (
            "Abstract",
            [
                (
                    f"This project analyzes {engagement['rows']:,} anonymized Facebook "
                    "posts and completes seven reproducible network-visualization "
                    "exercises. It combines cleaning, feature engineering, static and "
                    "interactive visualization, graph statistics, testing, and public "
                    "web delivery. Video posts have the largest observed mean total "
                    f"engagement ({engagement['top_post_type_mean_engagement']:,.2f}), "
                    "but the observational design does not establish causality."
                ),
                (
                    "Keywords: Facebook engagement, data visualization, social-network "
                    "analysis, NetworkX, Plotly, Python."
                ),
            ],
            None,
            None,
        ),
        (
            "1. Introduction and research questions",
            [
                "The study describes multidimensional engagement while preserving the "
                "distinction between real tabular observations and synthetic relationship "
                "graphs. It asks how engagement varies by content and time, how visual "
                "layout changes structural readability, and which canonical graph models "
                "capture specific social-network properties.",
                "A central methodological constraint is that the Facebook table contains "
                "no verified user-to-user edges. The empirical analysis therefore remains "
                "tabular; all assignment relationship graphs are explicitly synthetic.",
            ],
            None,
            None,
        ),
        (
            "2. Dataset, license, and ethics",
            [
                (
                    "Facebook Live Sellers in Thailand was authored by Nassim Dehouche "
                    "and distributed by UCI under CC BY 4.0. It records anonymized post "
                    f"engagement from {engagement['date_min'][:10]} through "
                    f"{engagement['date_max'][:10]}."
                ),
                "The official UCI archive was used because Kaggle credentials were not "
                "configured. The Kaggle mirror is documented but was not the acquisition "
                "route. No names, message text, or re-identification attempts are included.",
            ],
            None,
            None,
        ),
        (
            "3. Data cleaning and feature engineering",
            [
                (
                    f"The raw table contained {audit['initial_rows']:,} rows and "
                    f"{audit['initial_columns']} columns. Four empty placeholder columns "
                    f"were removed; {audit['duplicate_rows_removed']} duplicate rows and "
                    f"{audit['invalid_dates_removed']} invalid dates were found. The "
                    f"processed table contains {audit['final_rows']:,} rows and "
                    f"{audit['final_columns']} columns."
                ),
                (
                    "Total engagement equals reactions plus comments plus shares. Ratio "
                    "features use zero-safe division. Temporal features include posting "
                    "hour, weekday, month, ISO week, weekend, and time-of-day. No engagement "
                    "rate is claimed because reach and impressions are absent."
                ),
            ],
            None,
            None,
        ),
        (
            "4. Exploratory engagement findings",
            [
                (
                    f"The data record {engagement['total_reactions']:,} reactions, "
                    f"{engagement['total_comments']:,} comments, and "
                    f"{engagement['total_shares']:,} shares. Mean total engagement is "
                    f"{engagement['mean_engagement']:,.2f}, while the median is "
                    f"{engagement['median_engagement']:,.2f}; the gap is consistent with "
                    "strong right skew."
                )
            ],
            {
                "title": "Table 1. Engagement summary by post type",
                "headers": [
                    "Type",
                    "Posts",
                    "Mean reactions",
                    "Mean comments",
                    "Mean shares",
                    "Mean total",
                ],
                "rows": type_rows,
                "widths": [0.75, 0.65, 1.1, 1.05, 0.95, 1.2],
            },
            (
                STATIC / "engagement_by_post_type.png",
                "Mean engagement components by post type.",
                "Grouped bar chart of mean reactions, comments, and shares by post type.",
            ),
        ),
        (
            "5. Distribution, correlation, and time",
            [
                (
                    f"The upper Tukey fence flags {audit['outlier_count']:,} posts rather "
                    "than deleting them. Rank correlations and log-transformed distributions "
                    "are used because extreme posts make raw-count views difficult to read."
                ),
                (
                    f"The largest observed median engagement occurs at "
                    f"{engagement['best_median_posting_hour']:02d}:00, but content mix, "
                    "seller behavior, and seasonality are plausible confounders."
                ),
            ],
            None,
            (
                STATIC / "engagement_distribution.png",
                "Log-transformed total-engagement distributions by post type.",
                "Histogram comparison of log transformed engagement distributions.",
            ),
        ),
        (
            "6. Graph representation and visualization methodology",
            [
                "Adjacency matrices support exact pairwise lookup; node-link diagrams "
                "emphasize paths, clusters, bridges, and hubs. Visual encodings are held "
                "constant during layout comparison so that topology-driven placement is "
                "the primary changing variable.",
                "Force-directed algorithms map graph-theoretic relationships to proximity, "
                "whereas circular and random layouts do not optimize community readability.",
            ],
            None,
            None,
        ),
        (
            "7. Exercise 1 - Weighted adjacency representations",
            [
                (
                    "The G_transport matrix stores route distances in kilometers and is "
                    f"symmetric: {exercises['exercise_1']['matrix_symmetric']}. Symmetry "
                    "follows from undirected equal-weight edges; a directed or directionally "
                    "weighted network could be asymmetric."
                )
            ],
            None,
            None,
        ),
        (
            "8. Exercise 2 - Six-layout comparison",
            [
                "Kamada-Kawai is selected as the clearest layout for this exact 15-node "
                "G_ppi realization because it minimizes pairwise distance stress and "
                "makes ring locality plus rewired shortcuts legible. The measured average "
                f"clustering is {exercises['exercise_2']['average_clustering']:.3f}; no "
                "layout can reveal triangle-based clustering that is absent. Spring is a "
                "close alternative, and the judgment is not universal."
            ],
            None,
            (
                STATIC / "g_ppi_layout_comparison.png",
                "Six layouts of the identical synthetic G_ppi graph.",
                "Comparison of spring, circular, shell, spectral, Kamada-Kawai, and random layouts.",
            ),
        ),
        (
            "9. Exercise 3 - Student-course bipartite network",
            [
                (
                    f"The stored CSV tables form a valid bipartite graph with "
                    f"{exercises['exercise_3']['enrollments']} enrollments. "
                    f"{exercises['exercise_3']['most_popular_course']} is most popular, "
                    f"and {exercises['exercise_3']['most_enrolled_student']} takes the "
                    "largest number of courses."
                ),
                exercises["exercise_3"]["pattern"],
            ],
            None,
            (
                STATIC / "student_course_bipartite_graph.png",
                "Synthetic student-course enrollment network.",
                "Bipartite graph with student circles and course squares.",
            ),
        ),
        (
            "10. Exercise 4 - Weighted Barabasi-Albert graph",
            [
                (
                    f"All {exercises['exercise_4']['edges']} edges received seeded integer "
                    f"weights from {exercises['exercise_4']['minimum_weight']} to "
                    f"{exercises['exercise_4']['maximum_weight']}. Width changes tie "
                    "salience but does not redefine degree-based hubs. Random weights "
                    "demonstrate encoding rather than empirical importance."
                )
            ],
            None,
            (
                STATIC / "barabasi_albert_weighted.png",
                "Barabasi-Albert graph with normalized edge-width encoding.",
                "Weighted synthetic scale-free graph with thicker high-weight edges.",
            ),
        ),
        (
            "11. Exercise 5 - Generative-model comparison",
            [
                "Watts-Strogatz best captures high clustering and short paths; "
                "Barabasi-Albert best captures hubs and heterogeneous degree. A realistic "
                "social network may combine both, so none is universally best. "
                "Erdos-Renyi remains a useful homogeneous random baseline."
            ],
            {
                "title": "Table 2. Statistical comparison of Section 3 models",
                "headers": [
                    "Model",
                    "Nodes",
                    "Edges",
                    "Density",
                    "Clustering",
                    "Avg. path",
                    "Max degree",
                ],
                "rows": model_rows,
                "widths": [1.65, 0.55, 0.55, 0.7, 0.75, 0.75, 0.75],
            },
            (
                STATIC / "generative_models_degree_distribution.png",
                "Degree distributions of the three Section 3 models.",
                "Side-by-side degree histograms for three synthetic graph models.",
            ),
        ),
        (
            "12. Exercise 6 - Interactive node-color dashboard",
            [
                "The Plotly dashboard preserves node positions while a dropdown switches "
                "between categorical interest-group color and continuous in-degree color. "
                "Hover information reports node ID, group, in-degree, and out-degree, and "
                "edges remain visible in both modes."
            ],
            None,
            None,
        ),
        (
            "13. Exercise 7 - Applied AI and Multimedia research graph",
            [
                exercises["exercise_7"]["interpretation"],
                "The graph is synthetic and demonstrates centrality interpretation rather "
                "than empirical evidence about a research community.",
            ],
            None,
            (
                STATIC / "domain_graph.png",
                "Synthetic applied-AI and multimedia research knowledge graph.",
                "Typed research knowledge graph with weighted semantic relationships.",
            ),
        ),
        (
            "14. Discussion",
            [
                "The empirical and synthetic components answer different questions. The "
                "Facebook table supports descriptive post comparison but not individual "
                "relationship inference. The synthetic graphs reveal how topology, layout, "
                "and encoding shape network interpretation.",
                "Mean engagement is influenced by extreme posts, so median summaries, log "
                "distributions, and outlier flags accompany it. Correlations remain "
                "associational and do not isolate algorithm, audience, or content effects.",
            ],
            None,
            None,
        ),
        (
            "15. Limitations and ethical considerations",
            [
                "The data end in 2018, represent ten Thai sellers, and omit reach, "
                "impressions, followers, campaign spend, page identity, and content text. "
                "Results may not generalize across settings or time.",
                "The project preserves anonymization, reports aggregate findings, avoids "
                "re-identification, makes no unsupported causal claims, and clearly labels "
                "every dummy graph as synthetic.",
            ],
            None,
            None,
        ),
        (
            "16. Conclusion, recommendations, and future work",
            [
                "Video posts have the largest observed mean engagement, Kamada-Kawai most "
                "clearly presents the supplied small-world graph, weighted encoding "
                "separates tie salience from centrality, and the model comparison shows "
                "that social-network realism is multidimensional.",
                "Future work should add ethically collected reach denominators, multiple "
                "seller populations, repeated graph simulations, uncertainty intervals, "
                "content representations, and user testing of dashboard accessibility.",
            ],
            None,
            None,
        ),
    ]


def build_pdf(summary: dict[str, Any], path: Path) -> None:
    """Create a compact PDF fallback from the same verified summary."""

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=29,
            textColor=colors.HexColor("#17324D"),
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )
    document = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title="Visual Analytics and Network Analysis of Facebook Engagement Using Python",
        author=STUDENT["name"],
    )
    story = [
        Spacer(1, 1.2 * inch),
        Paragraph(
            "Visual Analytics and Network Analysis of Facebook Engagement Using Python",
            styles["CoverTitle"],
        ),
        Paragraph(
            f"{STUDENT['name']} | {STUDENT['id']}<br/>"
            f"{STUDENT['course_name']} ({STUDENT['course_code']}) | "
            f"{STUDENT['semester']}<br/>"
            f"{STUDENT['teacher']}, {STUDENT['designation']}<br/>"
            f"{STUDENT['department']}<br/>{STUDENT['university']}",
            styles["BodyText"],
        ),
        PageBreak(),
    ]
    figure_number = 1
    for title, paragraphs, table_spec, figure_spec in _docx_sections(summary):
        story.append(Paragraph(title, styles["Heading1"]))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, styles["BodyText"]))
            story.append(Spacer(1, 0.08 * inch))
        if table_spec:
            rows = [table_spec["headers"], *table_spec["rows"]]
            table = Table(rows, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EEF3")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 7),
                        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AAB4BD")),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 0.12 * inch))
        if figure_spec and figure_spec[0].exists():
            story.append(
                Image(str(figure_spec[0]), width=6.3 * inch, height=3.9 * inch)
            )
            story.append(
                Paragraph(
                    f"Figure {figure_number}. {figure_spec[1]}",
                    styles["Italic"],
                )
            )
            figure_number += 1
    story.append(PageBreak())
    story.append(Paragraph("References", styles["Heading1"]))
    references = [
        "1. Dehouche, N. (2018). Facebook Live Sellers in Thailand [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R60S",
        "2. Dehouche, N. (2020). Dataset on usage and engagement patterns for Facebook Live sellers in Thailand. Data in Brief, 30, 105661. https://doi.org/10.1016/j.dib.2020.105661",
        "3. Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. Proceedings of SciPy 2008, 11-15.",
        "4. Barabasi, A.-L. (2016). Network Science. Cambridge University Press. http://networksciencebook.com/",
        "5. Pandas documentation. https://pandas.pydata.org/docs/",
        "6. Matplotlib documentation. https://matplotlib.org/stable/",
        "7. Plotly Python documentation. https://plotly.com/python/",
        "8. NetworkX documentation. https://networkx.org/documentation/stable/",
    ]
    for reference in references:
        story.append(Paragraph(reference, styles["BodyText"]))
        story.append(Spacer(1, 0.06 * inch))
    story.append(
        Paragraph("Appendix: Reproducibility and assumptions", styles["Heading1"])
    )
    story.append(
        Paragraph(
            "Run python main.py to rebuild the generated artifacts and pytest to "
            "validate the pipeline. The supplied teaching notebooks are "
            "source-identical. The official UCI archive was used because Kaggle "
            "credentials were unavailable. All assignment relationship graphs are "
            "explicitly synthetic.",
            styles["BodyText"],
        )
    )
    document.build(story)


def generate_reports(summary_path: Path = ANALYSIS_SUMMARY) -> dict[str, Path]:
    """Generate all requested report formats."""

    summary = _load_summary(summary_path)
    REPORT.mkdir(parents=True, exist_ok=True)
    markdown_path = REPORT / "report.md"
    docx_path = REPORT / "report.docx"
    pdf_path = REPORT / "report.pdf"
    markdown_path.write_text(build_markdown(summary), encoding="utf-8")
    build_docx(summary, docx_path)
    build_pdf(summary, pdf_path)
    return {"markdown": markdown_path, "docx": docx_path, "pdf": pdf_path}
