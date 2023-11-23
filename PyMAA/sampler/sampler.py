import numpy as np
from ..utilities.general import check_large_volume, calc_x0, DirectionSampler


def har_sample(n_samples, x0, directions, verticies):
    """ Hit-and-Run sampler
    Sample n_samples starting from x0
    n_samples: number of samples to draw
    x0: starting point
    directions: Directions that have
    been searched in with the MAA algorithm phase 1
    verticies: The verticies found by searching in
    directions with the MAA algorithm
    """
    
    
    for i in range(10):
        if not check_large_volume(directions, verticies, x0, tol=1000):
            print(f'x0 not in large volume. Trying again. i:{i}')
            x0 = calc_x0(directions, verticies)
        else:
            break
        
    # We want to represent the bounding hyperplanes as
    # normalvectors and offsets.
    # Offset is the distance from origo to the
    # plane in the normal direction.
    offsets = [directions[i]@(-verticies[i]) for i in range(len(directions))]
    A = -directions  # Matrix containing all normal vectors
    b = offsets  # vector of offsets

    # Initialize parameters
    x_i = x0
    samples = np.empty((n_samples, len(x0)))
    dir_sampler = DirectionSampler(len(x0))
    directions = dir_sampler.draw_dir(n_samples)
    for j in range(n_samples):
        direct_i = directions[j]
        # Distances from x_i to bounding planes in direction direct_i
        t_range = (b-A@x_i)/(A@direct_i)
        filt_max = A@direct_i > 0
        filt_min = A@direct_i < 0
        lambda_max = min(t_range[filt_max])  # Maximum stepsize
        lambda_min = max(t_range[filt_min])  # Minimum stepsize
        lambda_i = np.random.uniform(lambda_min, lambda_max, 1)
        x_new = x_i+direct_i*lambda_i
        
        samples[j, :] = x_new
        x_i = x_new    

    return samples

def bayesian_sample(n_samples, vertices):
    '''
    Bayesian Bootstrap sampler. Uses convexhull, so it is mainly useful for 
    spaces of less than 10 dimensions.
    Partially from https://stackoverflow.com/questions/59073952/how-to-get-uniformly-distributed-points-in-convex-hull
    '''
    import random
    import numpy as np
    from numpy.linalg import det
    from scipy.spatial import Delaunay
    from scipy.spatial import ConvexHull
    
    dims = vertices.shape[-1]                     # Determine dimension of simplexes
    hull = vertices[ConvexHull(vertices).vertices]  # Find MGA points
    deln = hull[Delaunay(hull).simplices]       # Split MGA-hull into simplexes

    vols = np.abs(det(deln[:, :dims, :] - deln[:, dims:, :])) / np.math.factorial(dims) # Calculate volume of simplexes   
    
    #### Find number of samples pr. simplex from their volume
    samples_pr_simplex = [None] * vols.shape[-1]
    for k in range(vols.shape[-1]):    
        samples_pr_simplex[k] = int(np.round(vols[k]/vols.sum()*n_samples))
    
    #### Find random samples
    samples = np.zeros(shape=(sum(samples_pr_simplex),dims))
    counter = 0
    for l in range(vols.shape[-1]):
            for ll in range(samples_pr_simplex[l]):
               
                #### Find random vector which == 1
                a_list = [0,1]
                for i in range(dims): 
                    a_list.insert(i+1, random.uniform(0, 1))
                    a_list.sort()
                
                r = [None] * (dims+1)
                for j in range(len(a_list)-1):
                    r[j] = a_list[j+1] - a_list[j]
                random.shuffle(r)
                
                #### Sample the space
                sample_x = np.zeros(shape=(1,dims))

                for k in range(deln.shape[1]):
                    sample_x = np.add(deln[l][k]*r[k], sample_x)
                           
                samples[counter] = sample_x
                counter = counter + 1
        
    return samples
