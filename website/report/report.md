# Visual Analytics and Network Analysis of Facebook Engagement Using Python

**Student:** S. M. Monowar Kayser

**Student ID:** 253-25-019

**Course:** Data Visualization (CSE628)

**Semester:** Summer 2026

**Teacher:** Sadat Hasan, Adjunct Faculty

**Department:** Department of Computer Science and Engineering

**University:** Daffodil International University

## Abstract

An analysis is presented of 7,050 anonymized Facebook posts from ten Thai fashion and cosmetics sellers, and the supplied graph-visualization teaching material is extended through seven reproducible exercises. Data cleaning, feature engineering, exploratory visualization, graph representations, layout comparison, bipartite modeling, weighted encoding, generative-model statistics, and interactive Plotly networks are combined. A total of 1,622,326 reactions, 1,581,710 comments, and 282,159 shares is recorded. The largest mean total engagement is observed for video posts (1,041.57), although a causal claim is not supported by the observational design. Symmetry is verified in the weighted `G_transport` adjacency matrix, while a trade-off is revealed by the model comparison: clustering and short paths are captured by Watts-Strogatz, whereas hubs and degree heterogeneity are captured by Barabasi-Albert. A reproducible academic artifact is produced with static figures, interactive HTML, executable notebooks, a responsive website, automated tests, and machine-readable analytical outputs.

**Keywords:** Facebook engagement, data visualization, social-network analysis, NetworkX, Plotly, graph layout, Python

## Contents

1. Introduction and research questions
2. Dataset and provenance
3. Tools and reproducibility
4. Data-cleaning methodology
5. Feature engineering
6. Exploratory data analysis
7. Graph representation, visualization, and evidence framework
8. Seven mandatory network exercises
9. Discussion
10. Limitations and ethical considerations
11. Conclusion and recommendations
12. Future work and critical implications
References and reproducibility appendices

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

The dataset is **Facebook Live Sellers in Thailand**, authored by Nassim Dehouche and distributed by the UCI Machine Learning Repository under CC BY 4.0 (Dehouche, 2018). The raw CSV contains 7,050 rows and 16 columns; four columns are entirely empty placeholders. Posts span 2012-07-15 through 2018-06-13. The official UCI file was used because Kaggle credentials were not configured; a Kaggle mirror is documented but was not used for acquisition. The accompanying study reports anonymized data collected from ten Thai fashion and cosmetics seller pages (Dehouche, 2020).

The selection is appropriate because it is medium-sized, includes numerical and categorical engagement variables, contains timestamps, is publicly licensed, and contains no names or message text. Its limitation is equally important: it does not contain reach, impressions, follower counts, page identity, or user-to-user interaction IDs.

## 3. Tools and reproducibility

Python is the primary language. Pandas performs data preparation, NumPy supports numerical operations, NetworkX constructs and measures graphs, Matplotlib creates 300-DPI static figures, Plotly produces standalone interactive HTML, SciPy supports NetworkX's Kamada-Kawai layout path, python-docx creates the editable report, ReportLab provides a PDF fallback, nbformat creates notebooks, and pytest validates the workflow. Fixed seed 42 controls every stochastic graph and layout where the API accepts a seed.

## 4. Data-cleaning methodology

The raw file was preserved unchanged. Column names were standardized; 4 entirely empty columns were removed; numeric engagement fields were coerced, checked for nonnegative values, and stored as integers; timestamps were parsed; categories were normalized; and duplicates were checked by full row and `status_id`. The pipeline removed 0 duplicate rows and 0 duplicate IDs. It removed 0 invalid timestamps and imputed 0 missing numeric values. The final analytical table contains 7,050 rows and 27 columns.

Outliers are flagged, not deleted, using the upper Tukey fence on total engagement (1,019.00); 972 posts exceed the threshold. This preserves genuine high-performing posts while making skew explicit.

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

The dataset is composed of 4,288 photos, 2,334 videos, 365 status posts, and 63 links. Total engagement of 3,486,195 is recorded; a mean of 494.50 and a median of 69.00 are obtained, indicating right skew. The largest observed median engagement is associated with 18:00 (377.00), but the association may be affected by content mix, seller behavior, seasonality, or other unobserved factors.

**Table 1. Engagement summary by post type**

| Post type | Posts | Mean reactions | Mean comments | Mean shares | Mean total engagement |
|---|---:|---:|---:|---:|---:|
| Video | 2,334 | 283.41 | 642.48 | 115.68 | 1,041.57 |
| Status | 365 | 438.78 | 36.24 | 2.56 | 477.58 |
| Link | 63 | 370.14 | 5.70 | 4.40 | 380.24 |
| Photo | 4,288 | 181.29 | 15.99 | 2.55 | 199.84 |

![Mean engagement components by post type](../visualizations/static/engagement_by_post_type.png)

*Figure 1. Mean reactions, comments, and shares by post type.*

![Engagement distributions](../visualizations/static/engagement_distribution.png)

*Figure 2. Log-transformed total-engagement distributions reveal substantial right skew.*

![Correlation heatmap](../visualizations/static/engagement_correlation.png)

*Figure 3. Spearman correlations describe monotonic association rather than causation.*

## 7. Graph representation and visualization methodology

An adjacency matrix offers exact pairwise lookup, while a node-link diagram emphasizes paths, clusters, bridges, and hubs. Force-directed layouts encode graph topology into geometric proximity; circular and random layouts mainly impose placement rules unrelated to community quality. Node size, color, and edge width are kept semantically consistent within each comparison to isolate the effect of layout.

### 7.1 Conceptual framework for engagement measurement

Engagement is treated as a family of observable platform actions rather than a direct measurement of attention, satisfaction, or persuasion. A reaction can be produced with comparatively little effort, whereas a comment or share may require additional cognitive or social commitment. Even this distinction is contextual: a short comment may be less consequential than a reaction from an influential account, and a share may be critical, supportive, or merely archival. The available table contains counts but no semantic evidence about motivation. Accordingly, the analysis preserves reactions, comments, and shares as separate variables before combining them into total engagement. The aggregate is useful for ranking overall activity, but it is not presented as a validated psychological scale.

The difference between exposure and response is also fundamental. An engagement rate normally requires a denominator such as reach, impressions, followers, or unique viewers. None is available in the source file. Dividing observed actions by an invented or inappropriate denominator would create false precision, so the project reports counts, composition ratios, and within-dataset comparisons instead. This constraint narrows the claims but improves their validity. It also explains why a post with many engagements cannot automatically be described as efficient: the number of people who had an opportunity to engage is unknown.

### 7.2 Evidence standards and reproducible design

The workflow follows a separation between source evidence, derived evidence, and presentation. The raw CSV is preserved and identified by SHA-256. Cleaning rules operate on a copy and produce an auditable processed table. Calculated statistics and graph metrics are then serialized in one machine-readable summary. Reports, notebook claims, and website text read from that summary instead of maintaining independent handwritten numbers. This design reduces the risk that a corrected metric remains stale in one publication surface. It also makes a discrepancy testable: a reported value can be traced to a specific JSON field and to the function that calculated it.

Reproducibility is understood as more than the presence of code. Paths are resolved from the repository root, stochastic operations use seed 42, graph parameters are recorded, notebooks are executed from clean kernels, and required artifacts are checked for existence and nontrivial size. The artifact manifest records hashes for the canonical data, tables, figures, interactive files, notebooks, and reports. These measures cannot guarantee that every software version will render pixels identically, but they make the analytical decisions and the delivered version observable and comparable.

The design also separates regeneration from verification. A pipeline can finish without proving that its outputs are correct, so completion is followed by independent checks: schema assertions, numerical cross-checks, notebook error inspection, document-structure audits, link validation, responsive browser review, and deployment status inspection. Failures are reported at the surface where they occur. For example, an analytical test cannot certify that a dropdown works, and a visual browser check cannot establish that a matrix used the correct edge-weight field. Layered verification prevents one successful tool from being treated as evidence for an unrelated requirement.

### 7.3 Data quality assessment and transformation rationale

The raw table contains 7,050 records and 16 columns. Four columns are empty across all rows and carry no analytical information; removing them is a structural correction rather than an imputation decision. Duplicate checks are performed both on complete rows and on `status_id`, because two identical records and two records sharing an identifier represent different quality concerns. The observed duplicate counts are 0 complete rows and 0 identifiers. Date parsing is validated before temporal features are produced, preventing malformed timestamps from silently entering hourly or monthly summaries.

Count variables are required to be numeric, finite, and nonnegative. Categorical labels are normalized so that spelling or capitalization does not split a post type into artificial groups. Missing-value handling is deliberately conservative: imputation is applied only where a defensible zero interpretation exists, and the audit records the number of affected values. The processed table is then validated against explicit invariants, including unique identifiers, complete engineered columns, nonnegative engagement, and finite ratios. These checks convert assumptions into executable conditions rather than leaving them as undocumented analyst judgment.

Extreme engagement is retained. The upper Tukey fence is 1,019.00, and 972 records exceed it. Deleting these observations would remove genuine high-performing posts and materially change the phenomenon under study. Instead, an outlier flag supports sensitivity-aware summaries, while log transformation makes distribution plots readable. Mean and median are reported together so that the influence of the long right tail remains visible.

### 7.4 Feature validity and analytical interpretation

Total engagement is defined as the sum of the dataset's authoritative reaction total, comments, and shares. Component reaction fields are retained for composition analysis and quality comparison, but they do not replace the documented total without evidence that the two constructs are identical. The comment-to-reaction and share-to-total ratios are calculated with a zero-safe operation. Returning zero when the denominator is zero avoids infinite values and preserves a clear interpretation: no observed denominator-supported ratio is available for that row.

Temporal features translate timestamps into posting hour, weekday, month, ISO week, weekend status, and broad time-of-day categories. They describe when posts were published, not when engagement occurred. A high median for a posting hour may reflect content selection, seller strategy, seasonal campaigns, or audience composition. The feature therefore supports descriptive scheduling analysis but not a causal recommendation that changing the clock time alone will improve results.

The low, medium, and high engagement bands are rank-based descriptive labels within this dataset. They are not universal performance benchmarks and should not be compared directly with another page or platform without recalibration. Similarly, the outlier indicator is a statistical flag rather than a judgment that a record is erroneous. These labels are useful for filtering and visual explanation only when their local definition remains visible.

### 7.5 Distribution-aware exploratory strategy

The 7,050 posts record 3,486,195 total engagements. The mean (494.50) is substantially larger than the median (69.00), demonstrating that a small proportion of posts contributes heavily to the aggregate. A mean-only comparison would therefore describe the economic weight of high observations but not the typical post. The report pairs means with medians, count distributions, and log-scaled views so that both questions remain answerable.

Post-type comparisons are observational. Video has the highest observed mean total engagement (1,041.57), but post type was not randomized. Seller identity, live-event context, promotion, topic, audience size, and the platform's historical ranking system may all affect the result. The finding is appropriately phrased as an association in the recorded sample. It can motivate a controlled content experiment, but it cannot substitute for one.

Spearman correlation is selected because it evaluates monotonic rank association without assuming normally distributed raw counts. Total engagement necessarily shares components with reactions, comments, and shares, so strong correlations with the total are partly mathematical. Correlation between components may also arise from a common exposure mechanism. The heatmap is therefore interpreted as a descriptive relationship map, not as evidence that one action causes another.

### 7.6 Graph representation and metric semantics

A graph is defined by its nodes, edges, direction, and attributes; the drawing is only one representation of that structure. Adjacency lists are efficient for neighbor inspection in sparse graphs, while matrices support exact pairwise lookup, linear-algebra operations, and symmetry tests. Node-link diagrams are effective for paths, hubs, bridges, and small-scale topology, but they become difficult to read as density and label count increase. The exercises use each form for the task it supports rather than treating visualization as decoration.

Metric meaning depends on the graph model. Degree counts incident ties, in-degree counts received directed ties, and PageRank distributes importance through linked neighbors. Betweenness identifies nodes on shortest paths, but weighted shortest paths require a distance. In the knowledge graph, semantic strength is transformed to inverse strength so that a strong relationship becomes a short effective distance. Using raw strength directly as distance would reverse the intended meaning and could change the ranking.

Connectivity also controls path interpretation. Average shortest path is undefined across disconnected components because no finite route joins every pair. The model comparison therefore reports whole-graph path length only for connected graphs and uses the largest connected component for the disconnected Erdos-Renyi realization. The scope is stored beside the value so that a reader cannot mistake the component result for a network-wide statistic.

### 7.7 Visual encoding and layout validity

Layout algorithms change coordinates, not topology. A spring layout uses attractive and repulsive forces, Kamada-Kawai minimizes a graph-distance stress objective, spectral layout uses eigenvectors, and circular, shell, or random placement applies different geometric constraints. Because the same graph can look clustered or dispersed under different coordinates, visual grouping must be checked against calculated community or clustering measures. In Exercise 2, node attributes, sizes, edge styles, labels, and figure dimensions are held constant so that placement is the controlled variable.

The supplied `G_ppi` realization has average clustering 0.000. Kamada-Kawai is selected because it gives the clearest distance-oriented account of ring locality and shortcuts, not because it reveals communities that the metric does not support. This distinction is important in academic graph drawing: an aesthetically separated region may be a layout artifact, while a visually dense region may reflect label placement rather than structural cohesion.

Color, size, shape, and width are assigned specific semantic roles. Categorical variables use distinct hues; ordered measures use a continuous scale; student and course partitions use separate node forms; and synthetic edge weight is encoded through width. Legends, captions, and hover text state these mappings. Redundant visual cues are used where they improve accessibility, while unnecessary three-dimensional effects and decorative encodings are avoided.

### 7.8 Static and interactive visualization roles

Static figures provide a stable scholarly record. They can be numbered, cited, printed, and compared without requiring a runtime. They are exported at high resolution with explicit titles, labels, legends, and captions. Interactive Plotly artifacts answer different needs: readers can inspect individual nodes and posts, zoom into the long tail, isolate categories, and switch encodings. The project therefore treats interactivity as an analytical affordance rather than a replacement for documented static evidence.

The node-color dashboard illustrates controlled interaction. Both modes retain the same coordinates and edge traces. Interest-group color is categorical, whereas in-degree color is continuous. Because geometry remains fixed, changes in perception can be attributed to the selected color variable rather than a simultaneous layout change. Hover fields disclose group, in-degree, and out-degree, enabling the reader to check the visual impression against exact values.

## 8. Mandatory hands-on network exercises

### 8.1 Exercise 1: Weighted adjacency representations

#### 8.1.1 Objective and analytical question

The relationship between an adjacency list and a weighted adjacency matrix was examined through the supplied `G_transport` network. Particular attention was given to whether the matrix was symmetric and to what that symmetry implied about the direction of the modeled routes.

#### 8.1.2 Graph construction and stored attributes

Seven Bangladeshi cities were represented by nodes, and nine teaching routes were represented by undirected edges. A distance in kilometers was stored in the `weight` attribute of every edge. The graph contains 7 nodes, 9 edges, and a density of 0.4286. Dhaka was connected to 6 other cities and therefore received the largest degree.

#### 8.1.3 Analytical procedure

A labeled adjacency list was produced from NetworkX neighbor iterators. A weighted matrix was generated with `nx.to_pandas_adjacency`, using the documented node order and edge `weight` attribute. Symmetry was tested by comparing the matrix with its transpose through `numpy.allclose`. A zero off the diagonal was interpreted as the absence of a recorded direct route.

#### 8.1.4 Verified results

**Table 2. Weighted adjacency matrix for `G_transport` (kilometers)**

| City | Dhaka | Chattogram | Sylhet | Khulna | Rajshahi | Barishal | Rangpur |
|---|---:|---:|---:|---:|---:|---:|---:|
| Dhaka | 0 | 264 | 247 | 209 | 256 | 170 | 300 |
| Chattogram | 264 | 0 | 350 | 0 | 0 | 0 | 0 |
| Sylhet | 247 | 350 | 0 | 0 | 0 | 0 | 0 |
| Khulna | 209 | 0 | 0 | 0 | 0 | 130 | 0 |
| Rajshahi | 256 | 0 | 0 | 0 | 0 | 0 | 130 |
| Barishal | 170 | 0 | 0 | 130 | 0 | 0 | 0 |
| Rangpur | 300 | 0 | 0 | 0 | 130 | 0 | 0 |

The symmetry test returned **True**. The Chattogram-Sylhet edge was the longest at 350 km, while the Khulna-Barishal edge was the shortest at 130 km. The sum of the nine unique edge distances was 2,056 km.

#### 8.1.5 Academic interpretation

Symmetry was produced because every route was encoded as an undirected edge with one shared weight. The distance from city u to city v was therefore written into both matrix cells (u,v) and (v,u). An asymmetric matrix would be expected under one-way travel or direction-dependent cost. The adjacency list was better suited to neighbor inspection, while the matrix was better suited to exact pairwise lookup and numerical validation.

#### 8.1.6 Limitations and verification evidence

The graph was treated as a classroom illustration rather than a complete transportation model. Road conditions, route alternatives, travel time, and geographic validation were outside its scope. Reproduction evidence was saved in `outputs/tables/g_transport_adjacency_matrix.csv`, and matrix symmetry is covered by an automated test.

### 8.2 Exercise 2: Six-layout comparison

#### 8.2.1 Objective and controlled comparison

Spring, circular, shell, spectral, Kamada-Kawai, and random layouts were compared for the same `G_ppi` topology. Node identity, size, color, edge set, labels, and figure scale were held constant so that only placement was changed.

#### 8.2.2 Graph construction

The graph was reproduced with `nx.watts_strogatz_graph(n=15, k=3, p=0.3, seed=42)` and relabeled from `P1` through `P15`. The realization contains 15 nodes and 15 edges, has density 0.1429, average degree 2.00, and diameter 8. Degrees range from 1 to 4. Connectivity was verified as **True**.

#### 8.2.3 Layout procedure and criteria

Readability was assessed through edge crossings, label separation, preservation of local ring structure, visibility of rewired shortcuts, and correspondence between graph distance and visual proximity. Layout appearance was not accepted as evidence of community structure.

#### 8.2.4 Verified visual result

![Six-layout comparison](../visualizations/static/g_ppi_layout_comparison.png)

*Figure 4. Six layouts of the identical synthetic `G_ppi` graph.*

Kamada-Kawai was selected for this realization because pairwise graph-distance stress was minimized and ring-like locality remained legible. Spring placement provided a close alternative. Circular and shell layouts provided orderly labeling but imposed geometry unrelated to distance optimization. Spectral placement emphasized eigenvector structure, while random placement provided no topology-aware organization.

#### 8.2.5 Critical interpretation

The measured average clustering coefficient was **0.000**. Triangle-based clustering was absent in this exact seeded realization despite use of a Watts-Strogatz generator. The figure therefore supports interpretation of locality and shortcuts, but it does not support a claim that visual communities or triangular clusters were discovered. This distinction demonstrates why layout inspection must be checked against calculated statistics.

#### 8.2.6 Limitations and verification evidence

Layout preference remains dependent on graph size, parameterization, task, and labeling requirements. Six individual figures and a combined comparison were saved under `visualizations/static/`. Graph order, size, connectivity, edge count, degree range, diameter, and clustering were recalculated from the generated object.

### 8.3 Exercise 3: Student-course bipartite network

#### 8.3.1 Objective and data design

A two-mode network was constructed so that enrollment could be represented without inventing student-to-student or course-to-course edges. The synthetic tables contain 12 students, 6 courses, and 40 enrollment records.

#### 8.3.2 Graph construction, analytical procedure, and validation

Students were assigned to partition 0 and courses to partition 1. An undirected edge was added only when an enrollment row linked the two partitions. Bipartiteness was verified through `nx.algorithms.bipartite.is_bipartite`, which returned **True**. The realized bipartite density was 0.5556.

#### 8.3.3 Degree results

**Table 3. Enrollment degree by course**

| Course | Student enrollments |
|---|---:|
| Data Visualization | 12 |
| Machine Learning | 7 |
| Social Network Analysis | 6 |
| Database Systems | 5 |
| Human-Computer Interaction | 5 |
| Research Methodology | 5 |

An average of 3.33 courses was assigned per student, while an average of 6.67 students was assigned per course. **Data Visualization** had the largest course degree (12), and **Imran Kabir** had the largest student degree (5).

#### 8.3.4 Visual result

![Student-course graph](../visualizations/static/student_course_bipartite_graph.png)

*Figure 5. Synthetic enrollment network with student circles and course squares.*

The two-column arrangement made partition membership explicit. Node shape and color distinguished entity type, and degree differences were visible through incident enrollment edges.

#### 8.3.5 Academic interpretation

Data Visualization bridges every represented major. Data Science students also concentrate in Machine Learning and Social Network Analysis, while Multimedia Technology students favor Human-Computer Interaction. Degree answered a different question in each partition: student degree represented course load, whereas course degree represented synthetic popularity. A one-mode projection was not used because derived ties were not required.

#### 8.3.6 Limitations and verification evidence

The names and enrollment records were generated solely for teaching. No conclusion was drawn about actual students or enrollment behavior. Source tables were saved under `data/generated/`, calculated degrees were saved in `outputs/tables/student_course_degree_summary.csv`, and partition validity is checked by an automated test.

### 8.4 Exercise 4: Weighted Barabasi-Albert visualization

#### 8.4.1 Objective and graph construction

The effect of edge-width encoding was examined on the supplied 100-node Barabasi-Albert graph. The topology was generated with `n=100`, `m=2`, and seed 42. It contains 100 nodes and 196 edges, with average degree 3.92 and maximum degree 36.

#### 8.4.2 Weight assignment procedure

Every edge received one reproducible integer weight from 1 through 10 through a separately seeded pseudorandom generator. The topology was copied before weighting, so the unweighted and weighted figures contain identical nodes and edges. Edge width was scaled from weight; degree and layout position were not recomputed from weight.

#### 8.4.3 Verified weight distribution

**Table 4. Frequency of assigned edge weights**

| Edge weight | Number of edges |
|---:|---:|
| 1 | 16 |
| 2 | 26 |
| 3 | 18 |
| 4 | 25 |
| 5 | 20 |
| 6 | 18 |
| 7 | 17 |
| 8 | 14 |
| 9 | 25 |
| 10 | 17 |

The range was 1-10, the mean was 5.388, the median was 5.0, and the population standard deviation was 2.852. Total assigned edge weight was 1,056.

#### 8.4.4 Visual result

![Weighted BA graph](../visualizations/static/barabasi_albert_weighted.png)

*Figure 6. Seeded edge weights represented by line width in the synthetic Barabasi-Albert graph.*

Thicker lines increased perceptual salience for high-weight edges, while the hub-and-spoke topology remained unchanged. The unweighted companion image permits a direct encoding comparison.

#### 8.4.5 Academic interpretation

Edge weight and node centrality were kept conceptually separate. A high-weight edge was not interpreted as a high-degree node, and a prominent hub was not assumed to possess high-weight incident ties. Weighted centrality would require the weight to be defined as strength, capacity, cost, or distance; such a definition was not justified for the random teaching weights.

#### 8.4.6 Limitations and verification evidence

The weights are synthetic and demonstrate encoding only. The complete edge table was saved in `outputs/tables/barabasi_albert_edge_weights.csv`. Automated checks verify node and edge counts, the 1-10 range, and deterministic assignment.

### 8.5 Exercise 5: Statistical comparison of generative models

#### 8.5.1 Objective, model construction, and parameters

Three mechanisms were compared under the supplied parameters: Erdos-Renyi G(30, 0.08), Watts-Strogatz WS(30, 4, 0.1), and Barabasi-Albert BA(30, 2), each with seed 42. Random mixing, local clustering with rewiring, and preferential attachment were thereby contrasted.

#### 8.5.2 Metric procedure

Node count, edge count, density, average degree, clustering, connectivity, component count, average shortest-path length, maximum degree, and degree standard deviation were calculated. For the disconnected Erdos-Renyi realization, path length was calculated only on the largest connected component; a misleading whole-graph value was not reported.

#### 8.5.3 Verified statistical results

**Table 5. Statistical comparison of the three seeded models**

| Model | Nodes | Edges | Density | Avg. degree | Clustering | Avg. path | Components | Max degree | Degree SD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Erdos-Renyi G(n,p) | 30 | 33 | 0.076 | 2.200 | 0.072 | 3.828 | 3 | 4 | 1.166 |
| Watts-Strogatz small-world | 30 | 60 | 0.138 | 4.000 | 0.346 | 2.984 | 1 | 5 | 0.632 |
| Barabasi-Albert scale-free | 30 | 56 | 0.129 | 3.733 | 0.300 | 2.182 | 1 | 18 | 3.521 |

![Generative-model degree distributions](../visualizations/static/generative_models_degree_distribution.png)

*Figure 7. Degree distributions for the three exact seeded realizations.*

#### 8.5.4 Model-by-model interpretation

The Erdos-Renyi realization produced three components, low clustering (0.072), and maximum degree 4; it served as a homogeneous random baseline. The Watts-Strogatz realization remained connected and produced the highest clustering (0.346) with a narrow degree distribution. The Barabasi-Albert realization remained connected, produced the shortest average path (2.182), and generated maximum degree 18 with degree standard deviation 3.521.

#### 8.5.5 Comparative conclusion

Watts-Strogatz captures clustering and short paths; Barabasi-Albert captures hubs and heterogeneous degree. A social network can require both properties, so no model is universally best. The small-world mechanism was better suited to local clustering and short-path interpretation, whereas preferential attachment was better suited to hub and degree-heterogeneity interpretation. Social-network realism was therefore treated as multidimensional.

#### 8.5.6 Limitations and verification evidence

Only one small seeded realization was compared per parameter set. Ranking may change across seeds, sizes, and parameters; repeated simulation with uncertainty intervals would be required for population-level inference. The comparison was saved in `outputs/tables/generative_models_comparison.csv`, and separate degree-distribution figures were generated for every model.

### 8.6 Exercise 6: Interactive node-color dashboard

#### 8.6.1 Objective and interaction design

An interactive view was produced so that one directed social graph could be interpreted through two node-color variables without a positional confound. Categorical color represents interest group, while a continuous Viridis scale represents in-degree.

#### 8.6.2 Graph construction and generation procedure

The supplied seeded logic produced 20 users and 52 directed follow edges. Directed density was 0.1368. Interest-group similarity increased selection probability during generation, and duplicate selections were removed before edge insertion.

#### 8.6.3 Group and degree results

**Table 6. Synthetic interest-group membership**

| Interest group | Users |
|---|---:|
| Music | 2 |
| Sports | 8 |
| Tech | 7 |
| Travel | 3 |

Mean in-degree was 2.60. In-degree ranged from 1 to 5, and out-degree ranged from 1 to 5. The three largest in-degree results were user_11 (5), user_12 (4), user_13 (4).

#### 8.6.4 Dashboard implementation and verification

The dropdown contains **Interest Group** and **In-Degree** modes. Node coordinates, edges, labels, and hover fields are preserved; only marker color, legend, and scale metadata are changed. Hover text reports identifier, group, in-degree, and out-degree. The stored position-preservation result is **True**.

![Network dashboard colored by interest group](../screenshots/network-toggle-before.png)

*Figure 8. Initial dashboard state with categorical interest-group color.*

![Network dashboard colored by in-degree](../screenshots/network-toggle-in-degree.png)

*Figure 9. Continuous in-degree color with unchanged node positions.*

#### 8.6.5 Academic interpretation

The categorical mode supports comparison of group mixing, while the continuous mode emphasizes incoming-tie popularity. Because position is fixed, perceptual change can be attributed to color rather than a new layout. The exercise demonstrates coordinated encoding rather than evidence about real social-media users.

#### 8.6.6 Limitations and verification evidence

The graph is synthetic. Arrowheads are not displayed in the Plotly line traces, so direction is conveyed through calculated degrees rather than edge-end markers. The artifact was saved as `visualizations/interactive/network_color_toggle_dashboard.html`, and both dropdown states were verified through browser testing.

### 8.7 Exercise 7: Research-domain knowledge graph

#### 8.7.1 Objective and semantic schema

A synthetic knowledge graph was constructed for Applied AI and Multimedia. Nodes were typed as research areas, methods, tools, applications, or outcomes. Edges received a named semantic relationship and an illustrative strength from 1 through 3.

#### 8.7.2 Graph construction and metric procedure

The graph contains 15 nodes and 21 undirected links. Density is 0.2000, average degree is 2.80, and connectivity was verified as **True**. Degree centrality, inverse-strength weighted betweenness, closeness, and strength-weighted PageRank were calculated. Edge distance was defined as (1 / strength) before shortest-path betweenness was evaluated.

#### 8.7.3 Verified centrality results

**Table 7. Five highest weighted-betweenness nodes**

| Node | Type | Degree | Betweenness | Closeness | PageRank |
|---|---|---:|---:|---:|---:|
| Recommendation Systems | Research area | 5 | 0.5385 | 0.5600 | 0.1297 |
| Artificial Intelligence | Research area | 3 | 0.2509 | 0.4667 | 0.0790 |
| Deep Learning | Method | 4 | 0.1923 | 0.4667 | 0.1011 |
| Computer Vision | Research area | 3 | 0.1667 | 0.4375 | 0.0795 |
| Graph Neural Networks | Method | 3 | 0.1612 | 0.5000 | 0.0630 |

**Recommendation Systems** received the largest weighted-betweenness value (0.5385).

#### 8.7.4 Visual result

![Research-domain graph](../visualizations/static/domain_graph.png)

*Figure 10. Synthetic Applied AI and Multimedia knowledge graph with typed nodes and weighted links.*

#### 8.7.5 Academic interpretation

Recommendation Systems is the strongest bridge by inverse-strength weighted betweenness, linking research themes, technical methods, and application outcomes. The graph is synthetic and demonstrates structural interpretation, not empirical evidence about a real research community. Centrality remained dependent on the modeled relationships: a method or application may appear prominent because otherwise separated categories are connected through it.

#### 8.7.6 Limitations and verification evidence

The nodes, relationships, and strengths were designed for demonstration and were not extracted from publications. The inverse-strength transformation assumes that a stronger semantic relationship represents a shorter effective distance; a different substantive meaning for strength would require a different transformation. Tables were saved under `data/generated/` and `outputs/tables/domain_graph_metrics.csv`, and both static and interactive visualizations were generated.

## 9. Discussion

The empirical and synthetic components answer different questions. The Facebook table supports descriptive comparison of observed posts; it does not reveal individual users, verified follower ties, or causal effects. The synthetic graphs instead demonstrate how topology, representation, layout, and visual encoding affect interpretation. Keeping these scopes separate prevents a common analytical error: inferring social relationships that the source data never recorded.

The engagement analysis shows a mixture of high-frequency photos and high-engagement videos. Mean comparisons are influenced by extreme posts, so medians, log distributions, and Tukey flags accompany them. Rank correlations are preferable to a sole reliance on Pearson correlation under strong skew, but they still describe association only.

## 10. Limitations and ethical considerations

The data end in 2018, cover ten sellers in Thailand, and may not generalize to other countries, sectors, platforms, or current Facebook behavior. Page identity and content text are absent, reducing both explanatory power and privacy risk. Platform algorithms, audience size, campaign spend, and post quality are unobserved confounders. The analysis avoids re-identification, preserves anonymization, reports only aggregated results, and distinguishes real observations from synthetic exercises.

## 11. Conclusion and recommendations

A reproducible bridge between tabular engagement analytics and network visualization is demonstrated. The highest observed mean engagement is associated with video posts, but the finding is descriptive. The supplied small-world teaching graph is presented most clearly by Kamada-Kawai, tie salience is distinguished from node centrality in the weighted BA exercise, and the multidimensional nature of social-network realism is revealed by the generative-model comparison.

Recommended next steps are to: (1) obtain ethically collected reach and impression denominators; (2) analyze multiple pages and time periods; (3) use repeated simulations and uncertainty intervals when comparing graph models; (4) test community detection separately from visual layout; and (5) retain the distinction between observed edges and synthetic teaching structures.

## 12. Future work

Future work could incorporate content embeddings, causal designs, hierarchical models for seller-level heterogeneity, temporal network models when genuine relational identifiers exist, and accessibility evaluation with classroom users.

### 12.1 Critical synthesis of empirical and synthetic evidence

The project contains two related but noninterchangeable forms of evidence. The Facebook analysis is empirical at the post level: rows are observed records and calculated values describe that sample. The network exercises are synthetic demonstrations of graph construction, measurement, and visual encoding. Their reproducibility does not make them empirical claims about Facebook users, students, transport, proteins, or research communities. Maintaining this boundary protects the report from a visually persuasive but unsupported narrative.

Taken together, the components show why data visualization requires both numerical and perceptual validation. A distribution plot explains why the mean and median differ; a matrix test verifies a symmetry that a node-link drawing merely suggests; clustering corrects an overly enthusiastic visual reading of layout; and a fixed-coordinate dropdown isolates the effect of color. Each major interpretation is therefore paired with a calculated value, controlled encoding, or explicit limitation.

### 12.2 Generalizability and uncertainty

External validity is limited by time, geography, industry, and platform context. The posts end in 2018 and originate from ten Thai fashion and cosmetics sellers. Facebook interfaces, ranking systems, audience behavior, and commercial practices have changed since collection. Results should therefore be read as a careful description of this dataset, not as a current global benchmark for social-media strategy.

The graph-model comparison is also conditional. Metrics from one 30-node seeded realization are exact for that realization but uncertain as estimates of a model's typical behavior. A stronger simulation study would repeat each parameter set across many seeds, summarize the metric distributions, and report confidence or percentile intervals. Parameter sweeps could then separate a mechanism's general tendency from a particular random draw.

Sensitivity analysis would also strengthen the empirical component. Post-type rankings could be recalculated after winsorization, within time periods, or with seller-level controls if stable page identifiers became available. Median and quantile regression could describe different parts of the engagement distribution without allowing the largest posts to dominate. Missing exposure denominators remain the most important obstacle: no transformation of the current counts can recover the unobserved population that saw each post. Future inference should therefore improve data collection before increasing model complexity.

### 12.3 Ethical, privacy, and academic-integrity safeguards

The source is anonymized and contains no post text, account names, or direct personal identifiers. The project does not attempt linkage, re-identification, or inference about protected characteristics. Aggregated reporting further reduces exposure. Synthetic people and relationships are labeled as such in data files, figures, notebooks, the website, and the report. These labels are not cosmetic: they prevent readers from confusing pedagogical structures with observed human behavior.

Academic integrity is supported through source attribution, explicit acquisition history, calculated rather than fabricated statistics, and reproducible code. The UCI dataset and its accompanying article are cited, software tools are acknowledged, and the unlicensed teaching package is not republished. The report distinguishes a Kaggle mirror from the actual UCI acquisition route and does not claim that credentials or an API were used when they were unavailable.

Accessibility is treated as an ethical property of communication. Figures use descriptive captions and alternative text; tables identify header rows; keyboard focus remains visible; and color is accompanied by labels, shape, position, or downloadable values when feasible. Interactive frames retain meaningful titles, while static equivalents preserve the central result for readers who cannot or prefer not to operate a dynamic chart. These measures do not constitute a complete accessibility certification, but they reduce avoidable barriers and make the evidential content less dependent on a single sensory channel.

### 12.4 Practical recommendations

For applied content analysis, future data collection should prioritize reach and impression denominators, stable page identifiers, content metadata, and campaign context. These variables would permit rate estimation, multilevel seller comparisons, and adjustment for exposure. A prospective design could rotate content formats or posting windows under controlled conditions. Until such evidence exists, video should be described as the highest-engagement observed category rather than a guaranteed intervention.

For network analysis, repeated simulations should precede general claims about model behavior. Community detection should be calculated independently of layout, and weighted metrics should document whether an edge attribute represents strength, capacity, probability, cost, or distance. Interactive views should preserve a stable reference state when comparing visual variables and should expose exact values through accessible text or downloadable tables.

For project maintenance, the canonical summary and artifact manifest should remain the only numerical publication interfaces. Changes to cleaning, graph parameters, or metric definitions should trigger the complete pipeline, notebook execution, report generation, website build, and cross-surface tests. A published release should be tied to a commit SHA so that the local project, repository, and GitHub Pages artifact can be compared unambiguously.

For teaching and assessment, each exercise should remain inspectable at three levels. The notebook shows how the calculation unfolds, the standalone source module shows reusable implementation, and the website connects code to output and interpretation. This layered presentation supports readers with different technical backgrounds while preserving one analytical result. Assessment should reward the justification of a representation and the accuracy of its limitation, not only the presence of an attractive graph.

### 12.5 Integrated design framework

The project adopts a question-first visualization framework. The empirical questions concern differences in recorded engagement across post types and time; the exercise questions concern graph structure, layout, weighting, and interaction. Those question classes require different evidence. Comparisons use aligned bars and tables, skewed outcomes use distributions and robust summaries, pairwise monotonic association uses a rank-correlation matrix, and network questions use matrices, node-link views, and calculated graph metrics. Selecting a representation from the analytical task prevents decorative novelty from becoming the governing design criterion.

Network science also distinguishes structure from its visual realization. Barabasi (2016) treats degree distributions, clustering, paths, and generative mechanisms as properties of graphs rather than of drawings. This report follows that distinction by calculating metrics with NetworkX and using layouts only to expose selected relationships. Hagberg, Schult, and Swart (2008) describe NetworkX as a platform for structural analysis; its role here is therefore computational, while Matplotlib and Plotly provide complementary static and interactive presentations. Recalculating metrics before rendering keeps visual appearance subordinate to the stored graph.

The empirical component is similarly anchored in provenance. Dehouche (2018, 2020) documents the Facebook Live Sellers in Thailand data and its engagement variables. The present study retains that observational unit and does not reinterpret posts as users or infer social ties. It adds reproducible cleaning, feature definitions, descriptive analysis, and visual communication, but it does not enlarge the evidential scope of the source. This source-to-claim traceability is especially important when a project combines a real table with synthetic graph exercises: the common software environment must not be mistaken for a common population or a shared causal design.

Finally, the communication design recognizes that reproducibility is both technical and rhetorical. A fixed seed and checksum reproduce an artifact, but a reader also needs definitions, captions, limitations, and accessible alternatives to understand what that artifact supports. The notebooks expose calculations, the report supplies sustained argument, the website supports navigation and interaction, and the machine-readable summary binds their numerical claims. Agreement among these layers is tested rather than assumed. The resulting architecture makes revision auditable: a change to a statistic must propagate from the canonical JSON through every presentation surface or cause a contract test to fail.

## References

Barabasi, A.-L. (2016). *Network science*. Cambridge University Press. http://networksciencebook.com/

Dehouche, N. (2018). *Facebook Live Sellers in Thailand* [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R60S

Dehouche, N. (2020). Dataset on usage and engagement patterns for Facebook Live sellers in Thailand. *Data in Brief, 30*, 105661. https://doi.org/10.1016/j.dib.2020.105661

Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. *Proceedings of the 7th Python in Science Conference*, 11–15.

Matplotlib Development Team. (2026). *Matplotlib documentation*. https://matplotlib.org/stable/

NetworkX Developers. (2026). *NetworkX documentation*. https://networkx.org/documentation/stable/

pandas development team. (2026). *pandas documentation*. https://pandas.pydata.org/docs/

Plotly Technologies Inc. (2026). *Plotly Python documentation*. https://plotly.com/python/

## Appendix A. Reproducibility and output map

Run `python main.py` to rebuild processed data, analytical tables, figures, interactive HTML, notebooks, summary JSON, and reports. Run `pytest` for automated validation. The raw CSV remains in `data/raw/`, the cleaned table in `data/processed/`, required exercise tables in `outputs/tables/`, figures in `visualizations/`, and interactive artifacts in both `visualizations/interactive/` and the deployed website.

## Appendix B. Assumptions

The supplied teaching notebooks contain source-identical graph definitions. Exercise 2 uses Kamada-Kawai as the preferred layout based on this exact realization. The Kaggle API was not used. `num_reactions` is treated as the dataset's authoritative reaction total while component sums are retained as a quality-control comparison.
