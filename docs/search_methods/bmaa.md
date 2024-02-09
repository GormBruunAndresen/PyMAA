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

# *class* PyMAA.methods.MAA(case)

Create a method object using the bMAA method, for a given case object

Example: `method = PyMAA.methods.bMAA(case)`

## find_optimum()

Find the optimum solution to the given case object. This is the same regardless of method chosen (MAA/bMAA)

**Returns**

- opt_sol - List containing the optimal values for each variable defined in the case

- obj - objective function value

- n_solved - solved PyPSA network

Example: `opt_sol, obj, n_solved = method.find_optimum()`

## bMAA.search_directions(n_samples, har_samples, n_workers = 4, max_iter = 30, tol = 0.99, save_tmp_results = True )

Performs the MAA analysis using the given method for the given case object.



**Parameters**

- n_samples - Maximum number of vertices to find before stopping.

- har_samples - Number of samples to draw each iteration, to determine next directions

- n_workers - Number of CPU threads to use for searching directions in parallel.

- max_iter - Maximum number of iterations before stopping

- tol - Stopping tolerance for ratio between upper and lower bound

- save_tmp_results - Whether to save results after each iteration. Saves newest results in tmp_results folder created in the working directory. Useful in case MAA analysis breaks down before completion.

**Returns**

| Name       | Type         | Description                                                |
| ---------- | ------------ | ---------------------------------------------------------- |
| vertices   | pd.DataFrame | The vertices of the polytope found during the MAA analysis |
| directions | pd.DataFrame | The directions associated with the found vertices          |
| stat       |              |                                                            |
| cost       |              |                                                            |

Example: `vertices, directions, _, _ = method.search_directions(n_samples = 500, n_workers = 16)`
