import chaospy
import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

class DirectionSampler():
    """Class for drawing random directions on the unit hypersphere. 
    Using Chaospy to draw quassi-random samples from a 
    joint normal distribution
    """
    def __init__(self, dim, rule='halton'):
        self.count = 0
        self.dim = dim
        self.dist = self.create_dist()
        self.rule = rule

    def create_dist(self):
        # Creates a joint distribution with dim normal distributions. 
        DD = []
        for i in range(self.dim):
            DD.append(chaospy.chaospy.Normal(0, 1))
        distribution = chaospy.J(*DD)
        return distribution

    def draw_dir(self, n=1):
        s = self.dist.sample(n+self.count, rule=self.rule)[:, self.count:]
        norm = np.linalg.norm(s, axis=0)
        s_scaled = s/norm
        self.count += n
        return s_scaled.T


def solve_direcitons(directions,
                     case,
                     client,
                     vertices,
                     sol_fullD,
                     stat,
                     cost):
    """ Solve the model for the given directions
    directions: Directions to search in 
    case: test case object
    client: DASK client
    vertices: Known vertices
    """
    dim = directions.shape[1]
    variables = list(case.variables.keys())[:dim]
    params = (directions, [variables for i in range(len(directions))])
    n_solved = client.map(case.search_direction, *params, pure=False)
    
    res = client.gather(n_solved)
    for res_i in res:
        if res_i[2] == 'ok':
            vertices = np.append(vertices, np.array([res_i[0]]), axis=0)
            
            sol_fullD = np.append(sol_fullD, 
                                  np.array([list(res_i[1].values())]), 
                                  axis=0)
            stat = np.append(stat, np.array([res_i[2]]), axis=0)
            cost = np.append(cost, np.array([res_i[3]]), axis=0)
        else:
            print('Direction not solved with sucess')
    
    return vertices, sol_fullD, stat, cost


def check_large_volume(directions, vertices, sample, tol=0):
    """ Given a set of directions and vertices, compute
    wheater a point (sample) is inside
    all the hyperplanes defined by
    normals (directions) and points (vertices)
    """
    dist = []
    for i in range(len(vertices)):
        dist.append(directions[i]@(sample-vertices[i]))

    distances = np.array(dist)
    passing = np.all(distances >= -tol)

    if not passing:
        idx = list(np.where(~(distances >= -tol))[0])
        print(f'violating constraint {idx}')
        print(distances[idx])

    return passing


def calc_x0(directions, vertices):
    n = vertices.shape[0]
    s = np.random.rand(n-1)
    s.sort()
    s = np.insert(s, [0, n-1], [0, 1])
    s = np.diff(s)

    x0 = np.sum(vertices.T*s, axis=1)
    return x0


def check_small_volume(points_nD, p):
    # Form equality matrix
    A_eq = np.append(points_nD.T, [np.ones(points_nD.shape[0])], axis=0)
    A_eq = np.round(A_eq, 13)
    b_eq = np.append(p, [1])
    # Objective function
    c = np.zeros(points_nD.shape[0])

    m = gp.Model('interVol')
    x = m.addMVar(shape=points_nD.shape[0],
                  vtype=GRB.CONTINUOUS,
                  name="x",
                  lb=0,
                  ub=1)
    m.addConstr(A_eq @ x == b_eq, name="c")
    m.setObjective(c @ x, GRB.MINIMIZE)
    m.setParam('LogToConsole', 0)
    m.optimize()
    m.Status

    return m.Status == 2

def calculate_cheb(vertices, directions):
    """
    Calculate the Chebyshev center and radius of a polytope defined by vertices and directions.

    Parameters:
    - vertices (pd.DataFrame): DataFrame containing the vertices of the polytope.
    - directions (pd.DataFrame): DataFrame containing the directions of the hyperplanes defining the polytope.

    Returns:
    - cheb_center (pd.DataFrame): DataFrame representing the coordinates of the Chebyshev center.
    - cheb_radius (float): The radius of the Chebyshev ball inscribed in the polytope.
    """
    import polytope as pt
    
    variables = vertices.columns
    vertices = vertices.values
    directions = directions.values
    
    if vertices.shape[1] <=5:
        #If the dimensions are below 7, use convexhull to get more accurate 
        # calculation of the Chebyshev center
        
        # Define polytope
        poly = pt.qhull(vertices)
        
    else:
        # If more than 7 dimensions, use less accurate hyperplanes to 
        # calculate Chebyshev center
    
        # Create inequality formulation of hyperplanes
        A = -directions
        b = np.sum(directions*-vertices, axis = 1)
        
        # Define polytope
        poly = pt.Polytope(A,b)
    
    cheb_center = pd.DataFrame([poly.chebXc], columns = variables)
    cheb_radius = poly.chebR
    
    return cheb_center, cheb_radius
