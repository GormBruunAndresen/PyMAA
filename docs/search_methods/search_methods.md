---
layout: default
title: 2 Search Methods
nav_order: 6
has_children: true
---

# Search methods

Any MAA analysis must perform a search in order to find the vertices of the near-optimal space.  The MAA methods available (MAA and bMAA) differ in how they choose the directions to search in.

Both methods start by minimizing and maximizing each variable, to establish the initial polytope.

## MAA Method

> First introduced in the paper [Modeling all alternative solutions for highly renewable energy systems](https://doi.org/10.1016/j.energy.2021.121294).

The MAA method relies on the computation of the convex hull of the polytope, defined by the vertices. The search directions are set as the face-normal directions, and the analysis stops when the volume of the convex hull stops changing significantly.

> **Pros**: Polytope is defined as the convex hull of the vertices, and search directions are likely yo yield good results.
> **Cons**: unsuited for high dimension (6+ dimensions) problems, because the QuickHull algorithm does not handle it well.

## bMAA Method

> First introduced in the paper Bounding the near-optimal solution space (Not yet published)

The bMAA method relies on h-representation of the polytope, and chooses search-directions based on which directions are likely to discover the most new space. The bMAA method stops at user-defined points, such as number of vertices found.

> **Pros**: Suitable for problems of any dimension
> **Cons**: Polytope not defined as the convex hull, but as the hyperplanes defined by the search directions and found vertices.
