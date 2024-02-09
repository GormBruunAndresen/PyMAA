---
layout: default
title: General
parent: Utilities
---

# General

### Table of contents

- [General functions](#general-functions)
- [PyMAA.utilities.general.calculate_cheb()](#pymaautilitiesgeneralcalculate_cheb)

## General functions

PyMAA has some general helper functions in the `general.py` file. These are helper functions for various operations, as well as some analysis functions.

## PyMAA.utilities.general.calculate_cheb()

Calculate the center and radius of the largest inscribed ball within the polytope (The Chebyshev center and radius). 

If the polytope is of dimension 5 or less, the convex hull will be used for calculation. For  6 or more dimensions, the hyperplanes will be used. 

Example: 

> ```python
>  from PyMAA.utilities.general import calculate_cheb
> 
>  cheb_center, cheb_radius = calculate_cheb(vertices, directions)
> ```

**Parameters**

| Name       | Type         | Description                                                                   |
| ---------- | ------------ | ----------------------------------------------------------------------------- |
| vertices   | pd.DataFrame | DataFrame containing the vertices of the polytope.                            |
| directions | pd.DataFrame | DataFrame containing the directions of the hyperplanes defining the polytope. |

**Returns**

| Name        | Type         | Description                                                     |
| ----------- | ------------ | --------------------------------------------------------------- |
| cheb_center | pd.DataFrame | DataFrame representing the coordinates of the Chebyshev center. |
| cheb_radius | float        | The radius of the Chebyshev ball inscribed in the polytope.     |
