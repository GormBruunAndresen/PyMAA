---
title: 1 Case setup
layout: default
nav_order: 2
---

# Case setup

### Table of contents

- [The Case object](#the-case-object)
- [*class* PyMAA.cases.pypsa\_to\_case(project_name, config, base_network_path, extra_func = None, variables = None, tmp_network_path = 'tmp/networks/tmp.h5', n_snapshots = 8760, mga_slack = 0.1)](#class-pymaacasespypsa_to_caseproject_name-config-base_network_path-extra_func--none-variables--none-tmp_network_path--tmpnetworkstmph5-n_snapshots--8760-mga_slack--01)
- [PyMAA.cases.Cube(dim,cuts)](#pymaacasescubedimcuts)
- [PyMAA.cases.CubeCorr(dim)](#pymaacasescubecorrdim)
- [PyMAA.cases.CrossPoly(dim)](#pymaacasescrosspolydim)

## The Case object

The case object is used to define an optimization problem as an object with the methods necessary to conduct an MAA analysis. This way, the MAA analysis can draw the needed methods from the case object.

To be used in an MAA analysis, any case must include at least the following methods:

**case.\_\_init\_\_()**, in which basic parameters of the MAA analysis is set, such as the project name, which variables to include in the MAA analysis, and the objective function slack.

**case.solve()**, which must provide a way to solve the network, and return the solution

**case.search_direction()**, which must provide a way to search the solution space in a given direction.

PyMAA has a built-in class for creating case objects from PyPSA networks, as well as classes for creating testcases for MGA and MAA analysis.

## *class* PyMAA.cases.pypsa\_to\_case(project_name, config, base_network_path, extra_func, variables, tmp_network_path, n_snapshots, mga_slack)

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

## PyMAA.cases.Cube(dim,cuts)

A synthetic tescase of testing MGA/MAA methods. The method creates an optimization problem with a solution space in the form of a cube sliced with n cuts. <br>

*dim:* Number of dimensions of the test case 
*cuts:* Number of cuts <br>

## PyMAA.cases.CubeCorr(dim)

A synthetic tescase of testing MGA/MAA methods. The method creates an optimization problem with a solution space in the form of a cube sliced by parallel planes to give the space strong correlations between variables.<br>

*dim:* Number of dimensions of the test case<br>

## PyMAA.cases.CrossPoly(dim)

A synthetic tescase of testing MGA/MAA methods. The method creates an optimization problem with a solution space in the form of the intersection of a hyperube and a cross-polytope. <br>

*dim:* Number of dimensions of the test case <br>
