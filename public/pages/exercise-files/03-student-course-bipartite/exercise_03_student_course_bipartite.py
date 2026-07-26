#!/usr/bin/env python
# coding: utf-8

# # Exercise 3: Student-course bipartite network
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


# ## Exercise 3 - Student-course bipartite network
# 
# **Objective.** Build a two-mode graph from stored synthetic CSV tables and identify course popularity and student course load.

# In[ ]:


import networkx as nx
from src.graph_generators import load_student_course_graph
from src.network_analysis import student_course_findings
student_graph, students, courses, enrollments = load_student_course_graph()
degree_table, student_result = student_course_findings()
print('Bipartite:', nx.algorithms.bipartite.is_bipartite(student_graph))
display(degree_table)
display(Image(filename=str(ROOT / 'visualizations' / 'static' / 'student_course_bipartite_graph.png'), alt='Synthetic student-course bipartite enrollment graph'))


# **Interpretation.** Degree represents course load for student nodes and synthetic popularity for course nodes. These meanings must not be conflated.
# 
# **Limitation.** Names, majors, courses, and enrollments are illustrative and do not describe actual Daffodil International University records.
