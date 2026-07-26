#!/usr/bin/env python
# coding: utf-8

# # Exercise 6: Interactive node-color dashboard
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


# ## Exercise 6 - Interactive node-color dashboard
#
# **Objective.** Preserve node positions while toggling color between categorical interest group and continuous in-degree.

# In[ ]:


from IPython.display import HTML, display

dashboard_path = (
    ROOT / "visualizations" / "interactive" / "network_color_toggle_dashboard.html"
)
dashboard_html = dashboard_path.read_text(encoding="utf-8")
print("Standalone size:", f"{dashboard_path.stat().st_size / 1024:.1f} KiB")
print(
    "Dropdown labels present:",
    all(
        label in dashboard_html
        for label in ["Color by Interest Group", "Color by In-Degree"]
    ),
)
display(
    HTML(
        '<a href="../../visualizations/interactive/network_color_toggle_dashboard.html" target="_blank">Open standalone dashboard</a>'
    )
)


# **Interpretation.** Fixed coordinates isolate the effect of color: the categorical view supports group-mixing inspection and the continuous view emphasizes incoming-tie popularity.
#
# **Limitation.** Plotly line traces do not show arrowheads; direction is communicated through in-degree and out-degree values.
