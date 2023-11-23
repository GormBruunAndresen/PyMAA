# PyMGA changes journal

##### 08/09

* **Created Bayesian Bootstrap sampler**

##### 01/09

* **Created examples**
  Created two examples with two different networks, one using extra_func to pass custom consttraints.

* **Cleanup**
  Cleaned up package, removed old temporary files, etc.

##### 31/8

- **Made it possible to pass `extra_functionality()` constraints to `pypsa_to_case()`** When creating a case object using the `pypsa_to_case()` class, it can now take an `extra_func()` function as an input. Any functions executed in `extra_func()` is passed to `solve_network()` and included when the simulation runs `n.lopf()`. This makes it possible to define custom constraints without diving into the files in the package and the `solve_network()` function.

- **Created `plot.py` in `PyMGA/utilities`** Created new file to hold plotting functions, to make visualization of near-optimal spaces easier. Implemented the `near_optimal_space_2D()` function to easily plot 2D slice of near-optimal space based on two chosen variables.

##### 30/8

- **Prepared .py for multiprocessing** Previously, the jupyter notebook could use the `search_directions()` function just fine, but executed .py scripts and spyder did not function. This has been fixed by adding `if __name__ == '__main__':` in the script or spyder before the code part that would start parallell processes.
- **Temporary solution to n_snapshots bug** The problem only arises for networks that do not have 8760 snapshots, as 8760 is hardcoded in some functions. Temporary solution is to only run networks of 8760 snapshots, and create a full fix later.
- **Created new pypsa_to_case.py file in PyMGA/utilities/cases** Previously, the `pypsa_to_case()` class was in `pypsa_testcase.py`, now it has been moved to its own file.

##### 29/8

- **Identified bug with n_snapshots** When running a network with fewer than 8760 snapshots, the snapshot weightings are set automatically, even if they should just be 1. This causes slightly wrong optimal systems, leading to wrong MAA results. Problem arises from the snapshot adjustments in the `write_network()` method of the `pypsa_to_case()` class in `PyMGA/cases/pypsa_testcast.py`

- **Removed PyPSA-EUR specific code** Removed a lot of PyPSA-Eur specific code from:
  
  - `solve_network()` function in `PyMGA/utilities/solve_network.py`
  
  - `pypsa_to_case()` class in `PyMGA/case/pypsa_testcase.py`

##### 28/8

- **Created `pypsa_to_case()` class** Created `PyPSA_to_case()` class as a copy of `PyPSA_case()` class in `pypsa_testcase.py`. Aim is to make `PyPSA_to_case()` a general class for translating pypsa networks into case objects for the MAA methods.

##### 22/8

- **Updated `setup.py` with `find_packages()`** The setup file could not find subpackages when installing. This is fixed by importing the `find_packages()` function from `setuptools` in the `setup.py` file, and using it to automatically find the subpackages.

- **Created `__init__.py` for utilities subpackage**

##### Before 22/8

- **Removed gurobi from `install_requires` list** While gurobi is required, if gurobi is installed using conda, it could not be found by pip. This resulted in an error, as `pip install` would check for required packages, and not be able to find or install gurobi, even if it is already installed. Removed gurobi from list to fix this, but better solution should be found.

- **Removed vresutils from `install_requires` list and `solve_network()` function, as it was pypsa-eur specific.** vresutils was found to be utilized for the specific PyPSA-Eur network. Usage and import removed, along with other PyPSA-Eur specific code.

- **Added vresutils to `install_requires` list in `setup.py`** vresutils is imported in `PyMGA/utilities/solve_network.py` but not included in `install_requires` list in `setup.py`, which results in an error when trying to run the installed package, as vresutils was not automatically installed.

- **Fixed missing `','` in install_requires list in `setup.py`** 
  Could not install as package due to missing comma in list.

- **Changed install instructions in `readme.md`** Changed install instructions, as running `pip install PyMGA` from the folder did not work. Instead changed to two different approaches for installing the package, easiest being to run `pip install .` from the folder with the `setup.py` file.
