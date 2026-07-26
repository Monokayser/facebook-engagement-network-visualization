#!/usr/bin/env python
# coding: utf-8

# # Exercise 7: Applied AI and Multimedia knowledge graph
#
# This independently readable exercise notebook contains its objective, complete Python implementation, calculated output, interpretation, and limitation. The clean and executed editions are generated from the same canonical cells.
#
# **Student:** S. M. Monowar Kayser (253-25-019)
# **Course:** Data Visualization (CSE628), Summer 2026

# In[ ]:


from pathlib import Path
import json
import sys
from IPython.display import HTML, Image, display

ROOT = Path.cwd().resolve()
while ROOT != ROOT.parent and not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
if not (ROOT / "pyproject.toml").exists():
    raise FileNotFoundError("Run this file inside the project checkout.")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SUMMARY = json.loads(
    (ROOT / "outputs" / "analysis_summary.json").read_text(encoding="utf-8")
)
print("Project root resolved successfully.")
print("Canonical summary loaded successfully.")


# ## Exercise 7 - Applied AI and Multimedia knowledge graph
#
# **Objective.** Build a typed, weighted graph from CSV files and calculate degree, inverse-strength betweenness, closeness, and PageRank.

# In[ ]:


from src.network_analysis import domain_metrics

domain_table, domain_result = domain_metrics()
display(domain_table.head(10))
print(
    "Top bridge:",
    domain_result["top_betweenness_node"],
    domain_result["top_betweenness_value"],
)
display(
    Image(
        filename=str(ROOT / "visualizations" / "static" / "domain_graph.png"),
        alt="Synthetic Applied AI and Multimedia research knowledge graph",
    )
)


# **Interpretation.** Recommendation Systems is the strongest bridge under inverse-strength weighted betweenness because it connects research themes, methods, and application outcomes.
#
# **Limitation.** The graph is illustrative and is not evidence extracted from publications or a real research community.
