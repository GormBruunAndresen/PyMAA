---
title: 3 Sampling
layout: default
nav_order: 7
has_children: true
---

# Sampling

Sampling the polytope evenly is often relevant. PyMAA has two methods of even sampling the polytope implemented, the Bayesian Bootstrap sampler and the Hit-and-Run sampler. 

## Bayesian Bootstrap sampling

> **Note:**
> Bayesian Bootstrap is not suited for high-dimension polytopes (6+ dimensions) because it relies on the v-representation by calculating the convex hull, but QuickHull cant handle high dimensions.

Bayesian Bootstrap sampling works by splitting the polytope into simplexes, and drawing samples from within these simplexes.

## Hit-and-Run sampling
> **Note:**
> Works in any directions, using h-representation of the polytope

Hit-and-Run sampling works by iteratively drawing lines in random directions within the polytope, taking a sample at a random point along the line and creating a new line in a random direction at the sampled point.
