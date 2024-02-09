---
layout: default
title: 2 Search Methods
nav_order: 6
has_children: true
---

# Search methods

Any MAA analysis must perform a search in order to find the vertices of the near-optimal space.  In PyMAA, this search is done by searching in a given direction. The MAA methods available differ in how they choose the directions to search in.

The methods all have a common starting starting directions to search, as each variable for the MAA analysis is minimized and maximized.

Here follows a quick overview of each method. For details, see the pages for each method.

## MAA Method

The MAA method relies on the computation of the convex hull of the polytope, defined by the vertices. The search directions are set as the face-normal directions, and the analysis stops when the volume of the convex hull stops changing significantly.

First introduced in the paper [Modeling all alternative solutions for highly renewable energy systems](https://doi.org/10.1016/j.energy.2021.121294).

**Pros**

- The convex hull of the polytope is well-defined by the quickhull algorithm

- Search directions are likely to yield good results 

**Cons**

* Cannot be used with 7-8 or more variables, depending on problem complexity. This is because the QuickHull algorithm cannot handle high-dimension problems.

## bMAA Method

The bMAA method relies on hyperplanes to define the polytope, and chooses search-directions based on which directions are likely to discover the most new space. The bMAA method stops at user-defined points, such as number of vertices found.

First introduced in the paper Bounding the near-optimal solution space (Not yet published)

**Pros**

- Can be used with problems in any dimension

**Cons**

- Result is not as conservative as the convex hull
