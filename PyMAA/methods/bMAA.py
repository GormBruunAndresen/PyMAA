import numpy as np
import os
import time
import pickle
import pandas as pd
from ..utilities.general import (solve_direcitons,
                                 DirectionSampler,
                                 check_large_volume,
                                 check_small_volume,
                                 calc_x0)
from ..utilities.dask_helpers import start_dask_cluster
from ..sampler.sampler import har_sample


class bMAA:
    def __init__(self, case):
        """
        """ 
        self.case = case
        self.dim = len(case.variables)
        
    def find_optimum(self):
        """ 
        """
        # Finding optimal solution
        start_time = time.time()
        print('\n PyMGA: Finding optimal system \n')
        self.obj, opt_sol = self.case.solve()
        self.opt_sol = pd.DataFrame([list(opt_sol.values())[:self.dim]], 
                                    columns = self.case.variables)
        end_time = time.time()
        print(f'\n PyMGA: Optimal system found \n obj. value: {round(self.obj,2)} \n Time used: {round(end_time - start_time,2)}\n')

        return self.opt_sol, self.obj
    
    def search_directions(self,
                          n_samples,
                          har_samples=5000,
                          n_workers=4,
                          max_iter=30,
                          tol=0.99,
                          save_tmp_results = True,
                          ):
        print('\n PyMGA: Searching near-optimal space using bMAA method \n')
        start_time = time.time()
        
        dim = self.dim
        dim_fullD = dim

        cluster, client = start_dask_cluster(workers=n_workers,
                                             try_slurm=False)

        stat = np.empty(shape=[0])
        cost = np.empty(shape=[0])
        directions = np.empty((0, 0))
        samples = None
        acc_small = None

        for i in range(max_iter):
            # Find directions
            if len(directions) == 0:
                print('initializing directions')
                new_directions = np.concatenate((np.diag(np.ones(dim)),
                                                -np.diag(np.ones(dim)),
                                                np.ones((1, dim)),
                                                -np.ones((1, dim))))
                directions = new_directions.copy()
                vertices = np.empty(shape=[0, dim])
                sol_fullD = np.empty(shape=[0, dim_fullD])
            else:
                print('searcing for new directions')
                max_iter = int(os.cpu_count())*4
                new_directions = find_new_directions(vertices,
                                                     directions,
                                                     samples,
                                                     acc_small,
                                                     client,
                                                     max_iter=max_iter)
                print(f'Found {len(new_directions)} new directions')

                if (len(directions)+len(new_directions)) > n_samples:
                    remaining_evaluations = n_samples-len(directions)
                    new_directions = new_directions[:remaining_evaluations]

                directions = np.append(directions, new_directions, axis=0)

            # Solve directions
            print(f'searching in {len(new_directions)} directions')
            vertices, sol_fullD, stat, cost = solve_direcitons(new_directions,
                                                                self.case,
                                                                client,
                                                                vertices,
                                                                sol_fullD,
                                                                stat,
                                                                cost)
            print('checking validity of samples')
            test = []
            for v in vertices:
                test.append(check_large_volume(directions,
                                               vertices,
                                               v,
                                               2000))
            violators = np.where(~np.array(test))[0]

            if len(violators) > 0:
                print(f'Deleting {len(violators)} violators')
                vertices = np.delete(vertices, violators, axis=0)
                directions = np.delete(directions, violators, axis=0)

            # Hit and run sample
            print(f'Hit and run sampling, {har_samples} samples')
            x0 = calc_x0(directions, vertices)
            samples = har_sample(har_samples, x0, directions, vertices)
            samples = samples.values

            # Find acceptance rate
            acc_small = []
            for i in range(len(samples)):
                acc_small.append(check_small_volume(vertices, samples[i]))

            acc_rate = np.mean(acc_small)

            print(f"""Iteration #{i},
                   total vertices {len(directions)},
                   acceptance rate {acc_rate:.3f}""")

            if acc_rate > tol:
                break

            if len(directions) >= n_samples:
                print('Max function evaluations reached. Stopping')
                break
            
        # Convert to dataframes
        vertices   = pd.DataFrame(vertices, columns = self.case.variables)
        directions = pd.DataFrame(directions, columns = self.case.variables)
            
        # Save temporary results 
        if save_tmp_results:
            tmp_results = {}
            tmp_results['project_name']   = self.case.project_name
            tmp_results['vertices']       = vertices
            tmp_results['directions']     = directions
            tmp_results['acc_rate']       = acc_rate
            tmp_results['Method']         = 'bMAA'
            
            # Create tmp folder if it does not exist
            if not os.path.exists('tmp_results'):
                os.makedirs('tmp_results')
            
            # Export tmp results as pickle
            with open(f'tmp_results/tmp_results_{self.case.project_name}.pkl', 'wb') as file:
                pickle.dump(tmp_results, file)
            
        end_time = time.time()
        print(f'\n PyMGA: Finished searching using bMAA method \n Time used: {round(end_time - start_time,2)} s \n')
        
        
        return vertices, directions, stat, cost


def find_new_directions(vertices,
                        directions,
                        samples,
                        acc_small,
                        client,
                        max_iter=64,
                        min_count=1):
    """ Find new directions that result in the largest 
    number of rejected samples
    vertices: The vertices found with MAA method
    directions: Directions used in the MAA 
    samples: Hit-and-Run samples
    client: DASK client 
    max_iter: maximum number of iterations
    min_count: minimum number of rejected samples
    returns
    new_direction: set of new directions
    """
    # Initialize 
    updated_directions = directions
    new_directions = np.empty((0, directions.shape[1]))
    updated_vertices = vertices
    count = np.inf
    n_iter = 0
    # Samples that are between the two bounds
    samples_between = samples[~np.array(acc_small)]
    samples_remaining = samples_between

    while count > min_count and n_iter < max_iter:

        res = select_best_direction(updated_vertices,
                                    updated_directions,
                                    samples_remaining,
                                    client,
                                    n_new=2000,
                                    )
 
        best_dir, samples_remaining, count, v_best = res

        updated_directions = np.concatenate((updated_directions, [best_dir]))
        new_directions = np.concatenate((new_directions, [best_dir]))
        updated_vertices = np.concatenate((updated_vertices, [v_best]))

        print(f'Rejecting {count},samples, #iter {n_iter},max k {0:.2f}')
        n_iter += 1 

    return new_directions


def select_best_direction(vertices,
                          directions,
                          samples,
                          client,
                          n_new=500,
                          n_samples=5000):
    """ Find the direction resulting in the largest number of rejected samples
    vertices: The vertices found with MAA method
    directions: Directions used in the MAA 
    samples: Hit-and-Run samples
    client: DASK client 
    n_new: number of random directions to test
    returns
    best_dir: best direction
    samples_remaining: samples not rejected by new direction
    count: number of rejected samples
    """

    # Random directions
    dir_sampler = DirectionSampler(vertices.shape[1], rule='random')
    test_directions = dir_sampler.draw_dir(n_new)

    counts = []

    # Find the vertex, furthest in direction of the dir_i
    idx = np.argmax(-test_directions@vertices.T, axis=1)
    v = vertices[idx]
    # Compute the number of samples rejected for each direction
    for i in range(n_new):
        samples_rejected = sum(test_directions[i]@(samples-v[i]).T < 0)
        counts.append(samples_rejected)

    # Select the best direction
    idx_best_dir = np.argmax(counts)
    best_dir = test_directions[idx_best_dir]
    v_best = vertices[idx[idx_best_dir]]
    
    # Fin the remaining samples
    samples_remaining = samples[[best_dir@(s-v_best) > 0 for s in samples]]
    count = counts[idx_best_dir]
    
    return best_dir, samples_remaining, count, v_best
    