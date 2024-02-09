---
title: Case setup
layout: default
nav_order: 2
---

# Case setup

# The basic Case object

The case object is used to define an optimization problem as an object with the methods necessary to conduct an MAA analysis. This way, the MAA analysis can draw the needed methods from the case object.

To be used in an MAA analysis, any case must include at least the following methods:

**case.\_\_init\_\_()**, in which basic parameters of the MAA analysis is set, such as the project name, which variables to include in the MAA analysis, and the objective function slack.

**case.solve()**, which must provide a way to solve the network, and return the solution

**case.search_direction()**, which must provide a way to search the solution space in a given direction.

PyMAA has a built-in class for creating case objects from PyPSA networks.

# *class* PyMAA.cases.pypsa\_to\_case(project_name, config, base_network_path, extra_func = None, variables = None, tmp_network_path = 'tmp/networks/tmp.h5', n_snapshots = 8760, mga_slack = 0.1)

A class which creates case objects from pypsa networks.

**Parameters**

- Project name - 

- config - 

- base_network_path - 

- extra_func - 

- variables - 

- tmp_network_path - 

- n_snapshots - 

- mga_slack
