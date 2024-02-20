# -*- coding: utf-8 -*-
"""
Created on 29/8/2023

@authors: 
    Lukas B. Nordentoft, lbn@mpe.au.dk
    Anders L. Andreasen, ala@mpe.au.dk
    
Description:
    Exmple use of PyMAA to explore a network with 3 buses.
"""

import PyMAA
import yaml
import numpy as np

#%%

#Setting __name__ to properly handle multiprocessing
if __name__ == '__main__':
    
    # Load options from configuration file
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
        
    # Load network
    network_path = 'example_3-bus_network.nc'
    
    # Number of points to find on the boundary of the near-optimal space
    n_boundary_points = 16

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
                 } 

    #### PyMAA #### -----------------------------------------------------------
    # PyMAA: Build case from PyPSA network
    case = PyMAA.cases.PyPSA_to_case(project_name = 'example',
                                     config = config, 
                                     base_network_path = network_path,
                                     variables = variables,
                                     mga_slack = 0.1,
                                     )
    
    # PyMAA: Choose MAA method
    method = PyMAA.methods.bMAA(case) 
    # method = PyMAA.methods.MAA(case) 
    # method = PyMAA.methods.MGA(case) 
    
    # PyMAA: Solve optimal system
    opt_sol, obj = method.find_optimum()
    
    # PyMAA: Search near-optimal space using chosen method
    vertices, directions, _, _ = method.search_directions(n_samples = n_boundary_points,
                                                           n_workers = 16)
    
    # PyMAA: Sample the near-optimal space
    # Bayesian bootstrap sampler, good up to around 8 dimensions
    # samples = PyMAA.sampler.bayesian_sample(1_000_000, vertices) 
    
    # Hit-and-Run sampler, slower but works in any dimensions.
    samples = PyMAA.sampler.har_sample(1_000_000, 
                                       x0 = np.zeros(len(vertices.columns)), 
                                       directions = directions, 
                                       vertices = vertices)

    


    #### Processing results #### ----------------------------------------------
    
    # Calculate Cheybshev center
    from PyMAA.utilities.general import calculate_cheb
    cheb_center, cheb_radius = calculate_cheb(vertices, directions) 
    
    # near-optimal slice plot
    from PyMAA.utilities.plot import near_optimal_space_slice

    near_optimal_space_slice(chosen_variables = ['x1', 'x2'], 
                              vertices = vertices,
                              samples = samples,
                              opt_solution = opt_sol,
                              )
    
    # Matrix plot
    from PyMAA.utilities.plot import near_optimal_space_matrix

    ax, fig = near_optimal_space_matrix(vertices = vertices,
                                        samples = samples,
                                        opt_solution = opt_sol,
                                        cheb_center = cheb_center,
                                        plot_vertices = True,
                                        )




      

