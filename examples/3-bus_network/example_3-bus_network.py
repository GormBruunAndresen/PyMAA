# -*- coding: utf-8 -*-
"""
Created on 29/8/2023

@authors: 
    Lukas B. Nordentoft, lbn@mpe.au.dk
    Anders L. Andreasen, ala@mpe.au.dk
    
Description:
    Exmple use of PyMGA to explore a network with 3 buses.
"""

import os
import sys

# Add parent folder to directory to load PyMGA package
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)

import PyMGA
from PyMGA.utilities.plot import near_optimal_space_matrix
import yaml

#%%

#Setting __name__ to properly handle multiprocessing
if __name__ == '__main__':
    
    # Create or load network
    network = 'example_3-bus_network.nc'
    
    n_boundary_points = 8
    
    # Load options from configuration file
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
        
    # Set MAA variables to explore
    variables = {'x1': ['Generator', # Component type
                       ['wind'],     # Carrier(s)
                       'p_nom',],    # Component attribute to explore
                 'x2': ['Generator',
                       ['coal'],
                       'p_nom',],
                  'x3': ['Generator',
                        ['solar'],
                        'p_nom',],
                  # 'x4': ['Store',
                  #       ['battery'],
                  #       'e_nom',],
                    } 

    #### PyMGA #### -----------------------------------------------------------
    # PyMGA: Build case from PyPSA network
    case = PyMGA.cases.PyPSA_to_case(config, 
                                     network,
                                     variables = variables,
                                     mga_slack = 0.1,
                                     )
    
    # PyMGA: Choose MAA method
    method = PyMGA.methods.bMAA(case)
    
    # PyMGA: Solve optimal system
    opt_sol, obj, n_solved = method.find_optimum()

    # PyMGA: Search near-optimal space using chosen method
    vertices, directions, _, _ = method.search_directions(n_boundary_points,
                                                           n_workers = 16)
    # PyMGA: Sample the identified near-optimal space
    # Bayesian bootstrap sampler, good up to around 8 dimensions
    bayesian_samples = PyMGA.sampler.bayesian_sample(1_000_000, vertices) 


    #### Processing results #### ----------------------------------------------
    # # Plot near-optimal space of Data and P2X
    all_variables    = list(variables.keys())
    #%%
    # Matrix plot
    near_optimal_space_matrix(variables = all_variables, 
                              vertices = vertices,
                              samples = bayesian_samples,
                              opt_solution = opt_sol,
                              )
    
    #%%
    
    from PyMGA.utilities.general import calculate_cheb
    cheb_center, cheb_radius = calculate_cheb(vertices, directions)

    from PyMGA.utilities.plot import near_optimal_space_slice
    
    near_optimal_space_slice(all_variables, ['x1', 'x2'], 
                             vertices, bayesian_samples,
                             opt_solution = opt_sol,
                             cheb_center = cheb_center,
                             )



      

