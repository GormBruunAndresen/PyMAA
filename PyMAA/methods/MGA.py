import numpy as np
from ..utilities.general import solve_direcitons, DirectionSampler
from ..utilities.dask_helpers import start_dask_cluster
import time
import pandas as pd


class MGA:
    def __init__(self, case):
        """
        """
        self.case = case
        self.dim = len(case.variables)

    def find_optimum(self):
        """
        Finds the cost optimal solution of the case object given
        """
        # Finding optimal solution
        print('\n PyMGA: Finding optimal system \n')
        start_time = time.time()
        self.obj, opt_sol = self.case.solve()
        self.opt_sol = pd.DataFrame([list(opt_sol.values())[:self.dim]], 
                                    columns = self.case.variables)
        end_time = time.time()
        print(f'\n PyMGA: Optimal system found \n obj. value: {round(self.obj,2)} \n Time used: {round(end_time - start_time,2)}\n')

        return self.opt_sol, self.obj

    def search_directions(self, n_samples, n_workers=4):
        """
        Performs the MGA study on the case study.
        The method draws random search directions
        uniformly over the hypersphere.
        """

        print('\n PyMGA: Searching near-optimal space using MGA method \n')
        start_time = time.time()

        dim = self.dim

        cluster, client = start_dask_cluster(workers=n_workers,
                                             try_slurm=False)

        dim_fullD = len(self.case.variables)
        # variables = list(self.case.variables.keys())[:dim]
        vertices = np.empty(shape=[0, dim])
        directions = np.empty((0, 0))
        sol_fullD = np.empty(shape=[0, dim_fullD])
        stat = np.empty(shape=[0])
        cost = np.empty(shape=[0])

        # timer = time.time()

        # Direction sampler
        dir_sampler = DirectionSampler(dim)
        random_directions = dir_sampler.draw_dir(n_samples)
        # Concatenate directions including max/min directions
        directions = np.concatenate([np.diag(np.ones(dim)),
                                    -np.diag(np.ones(dim)),
                                    random_directions],
                                    axis=0)

        # logger.info(f'searching in {len(directions)} directions in total')

        max_runs_per_iter = 500
        n_direction = len(directions)
        slices = np.concatenate((np.arange(0,
                                 n_direction,
                                 max_runs_per_iter),
                                 [n_direction]))

        for i in range(len(slices)-1):
            idx_low = slices[i]
            idx_high = slices[i+1]
            directions_i = directions[idx_low:idx_high]
            # logger.info(f'searching in {len(directions_i)}
            # directions in total')
            vertices, sol_fullD, stat, cost = solve_direcitons(directions_i,
                                                                self.case,
                                                                client,
                                                                vertices,
                                                                sol_fullD,
                                                                stat,
                                                                cost)
        end_time = time.time()
        print(f'\n PyMGA: Finished searching using MGA method \n Time used: {round(end_time - start_time,2)} s \n')

        # Convert to dataframes
        vertices   = pd.DataFrame(vertices, columns = self.case.variables)
        directions = pd.DataFrame(directions, columns = self.case.variables)

        return vertices, directions, stat, cost
