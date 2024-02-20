# PyMAA

A Python module for Modeling All Alternatives analysis. 

This was originally a fork of [PyMGA](https://github.com/TimToernes/PyMGA), but has diverged with additon of new features.

## Documentation

See [the documentation page](https://gormbruunandresen.github.io/PyMAA/)

## Installation

###### Install with pip

Execute the following command:

```python
pip install PyMAA
```

A successfull install will return

```python
Successfully built PyMAA
Installing collected packages: PyMAA
Successfully installed PyMAA-0.1.X
```

The package is now available for system wide use

### Environemnt

If you encounter erros when importing PyMAA, use PyMAA from the PyMAA anaconda environment. The environment file "pymaa_environment.yml" in the repository can be installed by executing:

```python
conda env create -f pymaa_environment.yml
```

<!---
## PyMAA.methods

#### PyMAA.methods.MGA(case)

**PyMAA.methods.MGA.find_optimum()**   
Finds the cost optimal solution of the case object given

**PyMAA.methods.MGA.serach_directions(n_samples, n_workers)**   
Performs the MGA study on the case study. The method draws random search directions uniformly over the hypersphere.  

*n_samples:* The number of samples to draw  
*n_workers:* number of parallel process to start. Default=4

#### PyMAA.methods.MAA

**PyMAA.methods.MAA.find_optimum()**   
Finds the cost optimal solution of the case object given

**PyMAA.method.MAA.search_directions(self, n_samples, n_workers, max_iter)**

Runs the MAA algorithm documented in [Modeling all alternative solutions for highly renewable energy systems](https://doi.org/10.1016/j.energy.2021.121294)

*n_samples:* Maximum number of samples to draw  
*n_workers:* number of parallel process to start. Default=4  
*max_iter:* Maximum number of MAA iterations  

#### PyMAA.methods.bMAA<br>

**PyMAA.methods.bMAA.find_optimum()**<br>
Finds the cost optimal solution of the case object given

**PyMAA.methods.bMAA.serach_directions(n_samples, har_samples, n_workers, max_iter, tol)**<br>

*n_samples:* Maximum number of samples to draw  <br>
*har_samples:* Number of MAA samples to draw when computing acceptance rate and finding new directions. Default=5000  <br>
*n_workers:* number of parallel process to start. Default=4  <br>
*max_iter:* maximum number of iterations to perfom. Default = 30  <br>
*tol:* The acceptance rate required before terminating, unless n_samples is reached first. A number between 0-1. Default = 0.99  <br>

#### PyMAA.cases<br>

**PyMAA.cases.PyPSA_to_case()**<br>

General case for creating case objects from PyPSA networks.

*config:* Dict with solver options

*base_network_path:* path to a saved PyPSA network. must be saved as ```.nc``` file.

*extra_func:* Extra functionalities. Pass extra constraints here, as in PyPSA.

*variables:* Dict of variables to explore using the MAA analysis

*mga_slack:* Slack on objective function value to use for MAA analysis.

**PyMAA.cases.Cube(dim,cuts)**<br>
A synthetic tescase of testing MGA/MAA methods. The method creates an optimization problem with a solution space in the form of a cube sliced with n cuts. <br>

*dim:* Number of dimensions of the test case <br>
*cuts:* Number of cuts <br>

**PyMAA.cases.CubeCorr(dim)**<br>
A synthetic tescase of testing MGA/MAA methods. The method creates an optimization problem with a solution space in the form of a cube sliced by parallel planes to give the space strong correlations between variables.<br>

*dim:* Number of dimensions of the test case<br>

**PyMAA.cases.CrossPoly(dim)**<br>
A synthetic tescase of testing MGA/MAA methods. The method creates an optimization problem with a solution space in the form of the intersection of a hyperube and a cross-polytope. <br>

*dim:* Number of dimensions of the test case <br>
-->
