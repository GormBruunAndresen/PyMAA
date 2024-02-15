---
title: What is MAA?
layout: default
nav_order: 3
has_children: True
---

# What is Modelling All Alternatives (MAA)?

Modeling All Alternatives (MAA) is an analysis method for optimization problems, aimed at defining the near-optimal feasible space of a convex optimization problem. It is a branch of Modeling to Generate Alternatives (MGA).

The general MAA method was first presented in the paper [Modeling all alternative solutions for highly renewable energy systems](https://doi.org/10.1016/j.energy.2021.121294). More detail can be found in that paper.

This page serves as a walk-through of the overall method.

## The MGA constraint

To find the near-optimal space, it is necessary to determine what is near-optimal. To do this, the optimal solution and optimal objective value must be known. With the optimal objective value known, the MGA constraint is formualted and imposed on the optimization problem. The MGA constraint is:

$1) \qquad f(\mathbf{x}) \leq f(\mathbf{x}^*) \cdot (1+\epsilon)$

Where $f(\mathbf{x}$) is the objective function value, $f(\mathbf{x}^*)$ is the optimal objective function value, and $\epsilon$ is the percentage slack on the objective function value, which determines how much the objective value is allowed to deviate from the optimum.

The near-optimal space, $W$, can then be defined as a subspace of the feasible space, $X$, as:

$2) \qquad W = (\mathbf{x}|\mathbf{x} \in X, \quad f(\mathbf{x}) \leq f(\mathbf{x}^*) )$ 

## Searching for vertices

## Sampling
