#!/usr/bin/env python
# coding: utf-8

# # Exercise 4: Weighted Barabasi-Albert graph
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


# ## Exercise 4 - Weighted Barabasi-Albert graph
#
# **Objective.** Assign reproducible integer edge weights from 1 to 10 and encode them through line width without changing topology.

# In[ ]:


import pandas as pd

weights = pd.read_csv(ROOT / "outputs" / "tables" / "barabasi_albert_edge_weights.csv")
display(weights.head(10))
display(weights["weight"].describe())
display(
    Image(
        filename=str(
            ROOT / "visualizations" / "static" / "barabasi_albert_weighted.png"
        ),
        alt="Barabasi-Albert graph with edge weight encoded through width",
    )
)


# **Interpretation.** Width changes the salience of selected ties, but random edge weights do not redefine which nodes are degree hubs. A weighted centrality measure would require a justified strength or distance meaning.
#
# **Limitation.** The weights demonstrate visual encoding only.
