---
layout: default
title: Bayesian Bootstrap sampling
parent: 3 Sampling
---

# Bayesian Bootstrap Sampling

### Table of contents

- [Bayesian Bootstrap description](#bayesian-bootstrap-description)
- [PyMAA.sampler.bayesian_sample()](#pymaasamplerbayesian_sample)

## Bayesian Bootstrap description

> **Note:** Bayesian Bootstrap is not suited for high-dimension polytopes (6+ dimensions) because the convex hull must be calculated, and QuickHull cant handle high dimensions.

Bayesian Bootstrap sampling works by calculating the convex hull representation of the polytope. Then, all simplexes that constitude the convex hull are sampled. The simplexes are obtained using Delaunay Triangulation.

The number of samples to draw from a simplex is determined by the share of the total volume for the simplex. 

To draw a sample, the vectors pointing to the simplex vertices are scaled with a coefficient from the *s* vector, and combined. The scaling coefficients in the *s* vector always sum to 1, which guarantees that the sample is within the simplex.

Bayesian Bootstrap sampling is illustrated here:

![](bayesian_example.png)

## PyMAA.sampler.bayesian_sample()

Sample evenly within a polytope using the Bayesian Bootstrap method.

> Example from `example_3-bus_network_MAA.py`: 
> 
> ```python
> from PyMAA.sampler import bayesian_sample
> 
> samples = bayesian_sample(n_samples = 1_000_000,
>                           vertices) 
> ```

**Parameters**

| Name      | Type         | Description                                    |
| --------- | ------------ | ---------------------------------------------- |
| n_samples | int          | Number of samples to draw.                     |
| vertices  | pd.DataFrame | DataFrame containing vertices of the polytope. |

**Returns**

| Name    | Type         | Description                             |
| ------- | ------------ | --------------------------------------- |
| samples | pd.DataFrame | DataFrame containing generated samples. |
