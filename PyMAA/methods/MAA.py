import os
import numpy as np
import time
import pickle
import pandas as pd
from scipy.spatial import ConvexHull
from ..utilities.general import solve_direcitons
from ..utilities.dask_helpers import start_dask_cluster


class MAA:
    def __init__(self, case):
        """
        """
        self.case = case
        self.dim = len(case.variables)

    def find_optimum(self):
        """ 
        """
        # Finding optimal solution
        print('\n PyMGA: Finding optimal system \n')
        start_time = time.time()
        self.obj, opt_sol, n_solved = self.case.solve()
        self.opt_sol = pd.DataFrame([list(opt_sol.values())[:self.dim]], 
                                    columns = self.case.variables)
        end_time = time.time()
        print(f'\n PyMGA: Optimal system found \n obj. value: {round(self.obj,2)} \n Time used: {round(end_time - start_time,2)}\n')

        return self.opt_sol, self.obj, n_solved

    def search_directions(self, 
                          n_samples, 
                          n_workers=4, 
                          max_iter=20,
                          save_tmp_results = True,
                          ):
        
        print('\n PyMGA: Searching near-optimal space using MAA method \n')
        start_time = time.time()
        
        dim = self.dim
        dim_fullD = dim

        cluster, client = start_dask_cluster(workers=n_workers,
                                             try_slurm=False)

        max_n_dir = int(os.cpu_count())*20
        old_volume = 0
        epsilon = 1
        directions_searched = np.empty([0, dim])
        hull = None

        vertices = np.empty(shape=[0, dim])
        directions = np.empty((0, 0))
        sol_fullD = np.empty(shape=[0, dim_fullD])
        stat = np.empty(shape=[0])
        cost = np.empty(shape=[0])

        for i in range(max_iter):  # epsilon>MAA_convergence_tol:

            if len(vertices) <= 1:
                # logger.info('initializing directions')
                directions = np.concatenate([np.diag(np.ones(dim)),
                                             -np.diag(np.ones(dim))],
                                            axis=0)
            else:
                directions = -np.array(hull.equations)[:, 0:-1]
                if len(directions) > max_n_dir:
                    directions = directions[np.random.choice(len(directions),
                                                             max_n_dir)]

            if (len(directions)+len(directions_searched)) >= n_samples:
                remaining_evaluations = n_samples - len(directions_searched)
                directions = directions[:remaining_evaluations]

            directions_searched = np.concatenate([directions_searched,
                                                  directions],
                                                 axis=0)

            # Run all searches in parallel using DASK
            vertices, sol_fullD, stat, cost = solve_direcitons(directions,
                                                                self.case,
                                                                client,
                                                                vertices,
                                                                sol_fullD,
                                                                stat,
                                                                cost)

            # logger.info('creating convex hull')
            try:
                hull = ConvexHull(vertices)
                # ,qhull_options='Qs C-1e-32')#,qhull_options='A-0.99')
            except Exception as e:
                print('did not manage to create hull first try')
                print(e)
                try:
                    hull = ConvexHull(vertices,
                                      qhull_options='Qx Q12 C-1e-32')
                except Exception as e:
                    print('did not manage to create hull second try')
                    print(e)

            delta_v = hull.volume - old_volume
            old_volume = hull.volume
            epsilon = delta_v/hull.volume

            print(f"""Iteration #{i},
                    total vertices {len(vertices)},
                    eps: {epsilon:.2f}""")
                    
            # Save temporary results 
            if save_tmp_results:
                tmp_results = {}
                tmp_results['project_name']   = self.case.project_name
                tmp_results['vertces']       = vertices
                tmp_results['directions']     = directions
                tmp_results['epsilon']        = epsilon
                tmp_results['Method']         = 'MAA'
                
                # Create tmp folder if it does not exist
                if not os.path.exists('tmp_results'):
                    os.makedirs('tmp_results')
                
                # Export tmp results as pickle
                with open(f'tmp_results/tmp_results_{self.case.project_name}.pkl', 'wb') as file:
                    pickle.dump(tmp_results, file)
                    
        end_time = time.time()
        print(f'\n PyMGA: Finished searching using MAA method \n Time used: {round(end_time - start_time,2)} s \n')

        # Convert to dataframes
        vertices   = pd.DataFrame(vertices, columns = self.case.variables)
        directions_searched = pd.DataFrame(directions_searched, columns = self.case.variables)

        return vertices, directions_searched, stat, cost
