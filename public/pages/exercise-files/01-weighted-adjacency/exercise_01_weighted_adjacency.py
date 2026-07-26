#!/usr/bin/env python
# coding: utf-8

# # Exercise 1: Weighted adjacency representations
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


# ## Exercise 1 - Weighted adjacency representations
# 
# **Objective.** Recreate the supplied `G_transport` graph, print its adjacency list, calculate the weighted matrix, and test symmetry.

# In[ ]:


import numpy as np
from src.graph_generators import build_transport_graph
from src.network_analysis import transport_representations
G_transport = build_transport_graph()
transport_matrix, transport_result = transport_representations(G_transport)
print('Adjacency list:')
for node, neighbours in transport_result['adjacency_list'].items():
    print(f'{node}: {neighbours}')
display(transport_matrix)
print('Symmetric:', np.allclose(transport_matrix, transport_matrix.T))


# **Interpretation.** The matrix is symmetric because every route is undirected and has one shared distance. A directed or direction-dependent transport graph could produce an asymmetric matrix.
# 
# **Limitation.** The seven-city graph is a teaching example rather than a complete or geographically validated route network.
