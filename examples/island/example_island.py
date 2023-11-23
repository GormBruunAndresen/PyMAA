# -*- coding: utf-8 -*-
"""
Created on 29/8/2023

@authors: 
    Lukas B. Nordentoft, lbn@mpe.au.dk
    Anders L. Andreasen, ala@mpe.au.dk
    
Description:
    Example case based on the North Sea Energy Island. Consists of an island 
    with wind, P2X and storage capacity, connected to several countries.
    This example include custom constraints being defined using extra_func.
"""

import PyMAA
from PyMAA.utilities.plot import near_optimal_space_matrix
import numpy as np
import yaml
import pandas as pd


if __name__ == '__main__':
    
    # Create or load network
    network = 'example_island_network.nc'
    
    # Define total island area
    total_area = 0.5*120_000 #[m^2]
    
    # Define area uses
    area_use = pd.Series( data = {'storage':  01.0,  #[m^2/MWh] Capacity
                                  'hydrogen': 02.1,  #[m^2/MW] capacity
                                  'data':     27.3,  #[m^2/MW] IT output
                                  })
    
    
    # Load options from configuration file
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
        
        
    # Set MAA variables to explore
    variables = {'x1': ['Generator',
                        ['P2X'],
                        'p_nom',],
                'x2': ['Generator',
                        ['Data'],
                        'p_nom',],
                'x3': ['Store',
                        ['Storage'],
                        'e_nom',]
                        } 
    
    
    # Define constraints to be passed to extra_functionalities in n.lopf()
    def extra_func(n, snapshots, mga_options):
        
        ### Define custom constraints
        def link_constraint(n):
            from pypsa.linopt import get_var, linexpr, join_exprs, define_constraints
            '''
            This function sets an upper limit for the sum of link capacities.
            '''
            
            # Chosen Link names
            link_names = ['Island_to_Denmark', 'Island_to_Norway', 'Island_to_Germany',
                          'Island_to_Netherlands', 'Island_to_Belgium',
                          'Island_to_United Kingdom']               
            
            # Get all link variables, and filter for only chosen links
            vars_links   = get_var(n, 'Link', 'p_nom')
            vars_links   = vars_links[link_names]
            
            # Set up left and right side of constraint
            rhs          = 3_000 # [MW] Maximum total link capacity
            lhs          = join_exprs(linexpr((1, vars_links))) #Sum of all link capacities
            
            # Define constraint and name it 'Sum constraint'
            define_constraints(n, lhs, '<=', rhs, 'Link', 'Sum constraint')
          
        
        def marry_links(n):
            from pypsa.linopt import get_var, linexpr, define_constraints
            '''
            Each country has a link to and from the island. This constraint
            ensures that these links behave as bidirectional links by 
            constraining the to always have the same capacity. 
            This is done for each country.
            '''
            
            # Get all link varuables
            vars_links   = get_var(n, 'Link', 'p_nom')
            
            # List of countries to which the island is connected.
            connected_countries =  [
                                    "Denmark",         
                                    "Norway",          
                                    "Germany",         
                                    "Netherlands",     
                                    "Belgium",         
                                    "United Kingdom"
                                    ]
            
            # loop through countries and define constraints
            for country in connected_countries:
                
                # Define left side as the capacity of the link from the island
                # minus the capacity of the link to the island.
                lhs = linexpr((1, vars_links['Island_to_' + country]),
                              (-1, vars_links[country + '_to_Island']))
                
                # Set up right side to be 0. forcing lnks to be equal
                rhs = 0
                
                # Set up constraint
                define_constraints(n, lhs, '=', rhs, 'Link', country + '_link_capacity_constraint')
        
        
        def area_constraint(n):
            from pypsa.linopt import get_var, linexpr, define_constraints
            '''
            This function constrains the area available to the technologies
            on the island. This is done by multiplying the area use [m^2/MW] 
            with the capacity for each technology taking up space on the island.
            '''
            
            # Get variables to include in constraint
            vars_gen   = get_var(n, 'Generator', 'p_nom')
            vars_store = get_var(n, 'Store', 'e_nom')
            
            # Apply area use on variable and create linear expression 
            lhs = linexpr(
                           (area_use['hydrogen'], vars_gen["P2X"]), 
                           (area_use['data'],     vars_gen["Data"]), 
                           (area_use['storage'],  vars_store['Storage'])
                          )
            
            # Define right side as total area
            rhs = total_area #[m^2]
            
            # Define constraint
            define_constraints(n, lhs, '<=', rhs, 'Island', 'Area_Use')
        
        ### Call custom constraints 
        link_constraint(n)
        marry_links(n)
        area_constraint(n)

    #### PyMAA ####
    # PyMAA: Build case from PyPSA network
    case = PyMAA.cases.PyPSA_to_case(config, 
                                      network,
                                      extra_func = extra_func,
                                      variables = variables,
                                      mga_slack = 0.1,
                                      n_snapshots = 8760)
    
    # PyMAA: Choose MAA method
    method = PyMAA.methods.MAA(case)
    
    # PyMAA: Solve optimal system
    opt_sol, obj, n_opt = method.find_optimum()
    
    # PyMAA: Search near-optimal space using chosen method
    vertices, directions, _, _ = method.search_directions(14, n_workers = 16)

    # # PyMAA: Sample the identified near-optimal space
    har_samples = PyMAA.sampler.har_sample(1_000_000, x0 = np.zeros(len(variables.keys())), 
                                            directions = directions, 
                                            verticies = vertices)
    
    bayesian_samples = PyMAA.sampler.bayesian_sample(1_000_000, vertices)


    # #### Process results ####
    # # Matrix plots using both sample types
    near_optimal_space_matrix(variables = list(variables.keys()), 
                              vertices = vertices, 
                              samples = har_samples,
                              opt_solution = opt_sol)
    
    near_optimal_space_matrix(variables = list(variables.keys()), 
                              vertices = vertices, 
                              samples = bayesian_samples,
                              opt_solution = opt_sol)
