---
layout: default
title: bMAA method
parent: Search Methods
---

# bMAA method

> The bMAA method was first introduced in the paper Bounding the near-optimal solution space (Not yet published).

The bMAA method (Bounded Modlling All Alterntaives) uses hyperplanes to define the polytope. Each vertex of the polytope is associated with a search direction. For each iteration, the upper and lower bounds of the polytope are calculated. By drawing a small number of samples (~5000) from within the polytope, the ratio of samples inside the upper bound and inside the lower bound is used to determine the next search direction.

 This continues iteratively, until the search is stopped by a user defined criteria. 

**Pros**

- Can be used with problems in any dimension

**Cons**

- Result is not as conservative as the convex hull

The bMAA method bounds are illustrated here:
![](bmaa_method_illustration.png)
