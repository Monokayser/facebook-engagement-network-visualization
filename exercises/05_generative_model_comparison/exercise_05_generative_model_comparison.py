#!/usr/bin/env python
# coding: utf-8

# # Exercise 5: Generative-model comparison
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
while ROOT != ROOT.parent and not (ROOT / 'pyproject.toml').exists():
    ROOT = ROOT.parent
if not (ROOT / 'pyproject.toml').exists():
    raise FileNotFoundError('Run this file inside the project checkout.')
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SUMMARY = json.loads((ROOT / 'outputs' / 'analysis_summary.json').read_text(encoding='utf-8'))
print('Project root resolved successfully.')
print('Canonical summary loaded successfully.')


# ## Exercise 5 - Generative-model statistics
# 
# **Objective.** Compare the exact seeded Erdos-Renyi, Watts-Strogatz, and Barabasi-Albert realizations using consistent structural metrics.

# In[ ]:


from src.graph_generators import build_generative_models
from src.network_analysis import compare_generative_models
model_table, distributions = compare_generative_models(build_generative_models())
display(model_table)
display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'generative_models_degree_distribution.png'), alt='Degree distributions of three seeded generative graph models'))


# **Interpretation.** Watts-Strogatz better represents clustering and short paths, whereas Barabasi-Albert better represents hubs and heterogeneous degree. Neither is universally closest to every social network.
# 
# **Limitation.** One small realization per model cannot characterize the full sampling distribution of the metrics.
