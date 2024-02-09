---
title: Quickstart
layout: default
nav_order: 4
---

# Quickstart

Performing an MAA analysis can be done with relatively few lines of code. Here are quickstart examples to get going.

## Quickstart with custom case object

```python

```

## Quickstart with PyPSA network

For a PyPSA network, the solver settings are imported as a config file (See examples for config files) and the variables are set up as a dictionary. 

The case object is then built using the relevant PyMAA class and the method object is created from the case. 

With the method object, the optimum is solved and then the near-optimal space is searched. 

With the vertices and directions found, the space can be sampled and analyzed.

```python
# Import PyMAA
import numpy as np
import yaml
import PyMAA

# Load config file containing solver settings
with open('config.yaml') as f:
        config = yaml.safe_load(f)

# Define dict of variables to explore with MAA analysis
variables = {'x1': ['Generator', # PyPSA Component type
                   ['wind'],     # PyPSA Carrier(s)
                   'p_nom',],    # PyPSA Component attribute to explore

             'x2': ['Generator',
                   ['coal'],
                    'p_nom',],

             'x3': ['Generator', 
                   ['solar'],
                    'p_nom',],
             } 

# PyMAA: Build case from PyPSA network
case = PyMAA.cases.PyPSA_to_case(project_name = 'example_project',
                                 config = config, 
                                 network_path = 'network_file.nc',
                                 variables = variables,
                                 mga_slack = 0.1,
                                 )
# PyMAA: Choose MAA method (Either MAA or bMAA) and find optimum
method       = PyMAA.methods.bMAA(case) 
opt_sol, obj = method.find_optimum()

# PyMAA: Search near-optimal space using chosen method. 
# Find vertices (v) and directions (d)
v, d, stat, cost = method.search_directions(n_samples = 32,
                                            n_workers = 16)

### ----- SAMPLING ----- #### -----------------------------------------
# PyMAA: Sample using Hit-and-Run sampler
samples = PyMAA.sampler.har_sample(n_samples = 1_000_000, 
                                   x0 = np.zeros(len(vertices.columns)), 
                                   directions = d, 
                                   vertices = v)

### ----- ANALYZING ----- #### ----------------------------------------
# Find Chebyshev center and radius
cheb_center, cheb_radius = PyMAA.utilities.general.calculate_cheb(v, d)

# Create Matrix plot
PyMAA.utilities.plot.near_optimal_space_matrix(vertices = v,
                                               samples = samples,
                                               opt_solution = opt_sol,
                                               cheb_center = cheb_center,
                                               )
```
