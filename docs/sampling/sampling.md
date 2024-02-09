---
title: 3 Sampling
layout: default
nav_order: 7
has_children: true
---

# Sampling

Sampling the polytope evenly is often relevant. PyMAA has two methods of even sampling the polytope implemented, the Bayesian Bootstrap sampler and the Hit-and-Run sampler. 

Here follows a quick overview. See the sampling method pages for detailed descriptions.

## Bayesian Bootstrap sampling

Bayesian Bootstrap sampling works by calculating the convex hull representation of the polytope. Then, all simplexes that constitude the convex hull are sampled. The simplexes are obtained using Delaunay Triangulation.

The number of samples to draw from a simplex is determined by the share of the total volume for the simplex. To draw a sample, the vectors pointing to the simplex vertices are scaled with a coefficient and combined. The scaling coefficients always sum to 1, which guarantees that the sample is within the simplex.

> **Note:**
> Bayesian Bootstrap is not suited for high-dimension polytopes (6+ dimensions) because the convex hull must be calculated, and QuickHull cant handle high dimensions.

## Hit-and-Run sampling

Hit-and-Run sampling works by taking a random starting point from within the polytope. Then, a random direction is drawn, and a line is created in the random direction which goes through the point. This line meets the boundary at two points. With the line defined, a sample is drawn from a random position along the line. 

The Hit-and-Run process then continues iteratively, where the sample point on the line and a new random direction is used to create another line from which a sample is drawn, and so on.
