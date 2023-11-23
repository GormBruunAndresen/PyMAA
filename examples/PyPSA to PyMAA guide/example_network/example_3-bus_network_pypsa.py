# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:32:24 2023

@authors: 
    Lukas B. Nordentoft, lbn@mpe.au.dk
    Anders L. Andreasen, ala@mpe.au.dk
    
    
Description:
    This is an example network which is exported for use with PyMAA to perform
    an MAA analysis. As an example network, the values of costs and other system parameters are
    chosen to produce a dynamic near-optimal space for illustrative purposes,
    and are not at all accurate.
    This system does not need to be solved, only exported as a .nc file for use
    with PyMAA. 
"""

import pandas as pd
import pypsa

# Load wind power capacity factors from a CSV file
wind_capacity_factors = pd.read_csv(r'wind_cf.csv', 
                                    index_col=0, sep=",")[:8760]

pv_optimal = pd.read_csv(r'pv_optimal.csv',index_col=0, sep=";")['DNK']['2016-12-31 23:00:00':'2017-12-31 23:00:00']


# Create a PyPSA network and set snapshots to cover 2023.
network = pypsa.Network()
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

# Add backup coal generator capacity
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

network.export_to_netcdf('example_3-bus_network.nc')

# OPTIONAL: Solve the network. Not needed for PyMAA.
# network.lopf(pyomo = False, 
#               solver_name = 'gurobi',
#               formulation="kirchhoff",
#               keep_shadowprices = True, # Keep dual-values
#               )

