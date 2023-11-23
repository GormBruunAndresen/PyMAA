# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:32:24 2023

@authors: 
    Lukas B. Nordentoft, lbn@mpe.au.dk
    Anders L. Andreasen, ala@mpe.au.dk
"""

import pandas as pd
import pypsa
from pypsa_netview.draw import draw_network

# Load wind power capacity factors from a CSV file
wind_capacity_factors = pd.read_csv(r'C:\Users\au592788\OneDrive - Aarhus universitet\Dokumenter\Github\Masters_Thesis_NorthSeaEnergyIsland\data\wind\wind_cf.csv', 
                                    index_col=0, sep=",")[:8760]

pv_optimal = pd.read_csv(r'C:\Users\au592788\Downloads\pv_optimal.csv',index_col=0, sep=";")['DNK']['2016-12-31 23:00:00':'2017-12-31 23:00:00']


# Create a PyPSA network
network = pypsa.Network()

# Set the snapshots for the year
network.set_snapshots(pd.date_range(start="2023-01-01", end="2023-12-31 23:00:00", freq="H"))

# Add buses
network.madd("Bus",
             ["DemandBus", "REBus", "CoalBus"])

# Add links
network.madd('Link',
             names = ['WindLink', 'CoalLink'],
             carrier = ['wind_ac', 'coal_ac'],
             bus0  = ['REBus', 'CoalBus'],
             bus1  = ['DemandBus', 'DemandBus'],
             p_nom_extendable = True)

# Add a wind generator with time-series capacity factors
network.add("Generator",
            "WindGenerator",
            bus="REBus",
            carrier = 'wind',
            p_nom_extendable = True,
            p_max_pu = wind_capacity_factors['electricity'].values, # Wind capacity factors
            capital_cost = 500,
            marginal_cost = 5) 

# Add a solar PV generator with time-series capacity factors
network.add("Generator",
            "SolarGenerator",
            bus="REBus",
            carrier = 'solar',
            p_nom_extendable = True,
            p_max_pu = pv_optimal.values, # Wind capacity factors
            capital_cost = 100,
            marginal_cost = 2)


# Add backup generator capacity
network.add('Generator',
            'CoalPlant',
            bus = 'CoalBus',
            carrier = 'coal',
            p_nom_extendable = True,
            capital_cost = 500,
            marginal_cost = 50,)


# Add a storage unit (battery)
network.add("Store",
            "Battery",
            bus="REBus",
            carrier = 'battery',
            e_nom_extendable = True,
            e_nom_max = 1_000_000,  # Nominal power capacity in MW
            marginal_cost = 5,
            )


# Add a load (demand)
network.add("Load",
            "ElectricityLoad",
            bus="DemandBus",
            p_set=1000)  # Hourly demand in MW (constant for simplicity)

# network.export_to_netcdf('example_3-bus_network.nc')

def extra_functionality(n, snapshots):
    from pypsa.linopt import get_var, linexpr, define_constraints
    ''' 
    Constraint which limits the wind power to not be more than 3% of objective 
    value
    '''
    
    vars_gen = get_var(n, 'Generator', 'p_nom')
    
    # rhs = n.objective * 0.03
    # lhs = linexpr( (n.generators.loc['WindGenerator']['capital_cost'], vars_gen['WindGenerator']) )
    
    lhs = linexpr( (1, vars_gen['WindGenerator']) )
    
    rhs = n.generators.p_nom_opt['CoalPlant'] * 1.9
    
    define_constraints(n, lhs, "<=", rhs, "GlobalConstraint", "wind_limit")


# Solve the network
network.lopf(pyomo = False, 
              solver_name = 'gurobi',
              formulation="kirchhoff",
              keep_shadowprices = True, # Keep dual-values
              keep_references = True,  
               extra_functionality = extra_functionality,
              )

draw_network(network, show_capacities = True)

