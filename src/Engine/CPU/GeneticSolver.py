from Engine.CPU.Solver import *
from Engine.CPU.Portfolio import *


class GeneticSolver(Solver):
    def __init__(self, data, param):
        super().__init__("GA")
        self.data  = data
        self.param = param

        self.parents: Portfolio
        self.childs = Portfolio(self.data, self.param, (param['n_pop_GA'], param['K']), init=False)


    ### Public method ######################################################
    @L
    def run(self, parents):
        self.parents = parents
        for idx_iter in range(self.param['max_iter_GA']):
            ## 1. Select parents
            self._select()

            self._recombination(self.parents.assets, self.childs.assets)
            self.childs.evaluate()

            exit()
    ########################################################################


    ''
    ### Private method #####################################################
    def _select(self):
        """Select top n_candidate chromosome"""
        self.parents.select_top(self.param['n_candidate_GA'])
    @staticmethod
    @L
    @njit
    def _recombination(assets, pop):
        NP, K = pop.shape
        for idx_pf in range(len(pop)):
            idx_parent1, idx_parent2 = np.random.choice(len(assets), 2, replace=False)
            bags = np.append(assets[idx_parent1], assets[idx_parent2])  # already random

            for i in range(K):
                while True:
                    asset = np.random.choice(bags)
                    if asset in pop[idx_pf]:
                        break
                    else:
                        pop[idx_pf, i] = asset
                        break
    ########################################################################
