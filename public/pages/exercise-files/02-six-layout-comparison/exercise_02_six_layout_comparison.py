#!/usr/bin/env python
# coding: utf-8

# # Exercise 2: Six-layout comparison
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


# ## Exercise 2 - Six-layout comparison
#
# **Objective.** Compare spring, circular, shell, spectral, Kamada-Kawai, and random placement while holding topology and styling fixed.

# In[ ]:


from IPython.display import Image, display
from src.graph_generators import build_ppi_graph, graph_metrics

G_ppi = build_ppi_graph()
display(graph_metrics(G_ppi))
display(
    Image(
        filename=str(
            ROOT / "visualizations" / "static" / "g_ppi_layout_comparison.png"
        ),
        alt="Six layouts of the same synthetic small-world graph",
    )
)


# **Interpretation.** Kamada-Kawai gives the clearest distance-oriented view of ring locality and rewired shortcuts for this realization. The calculated clustering coefficient is 0.000, so no layout can establish triangle-based clusters that are absent from the graph.
#
# **Limitation.** Layout preference depends on topology, scale, labels, and the reader's task; it is not a universal ranking.
