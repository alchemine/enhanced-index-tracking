from Engine.CPU.Solver import *


class GeneticSolver(Solver):
    def __init__(self, data, param):
        super().__init__("GA")
        self.data  = data
        self.param = param

    ### Public method ######################################################
    @L
    def run(self, chroms):
        self.chroms = chroms
        for idx_iter in range(self.param['max_iter_GA']):
            ## 1. Select parents
            parents = self._select()

    ########################################################################


    ''
    ### Private method #####################################################
    def _select(self):
        """Select top n_candidate chromosome"""
        assets = self.chroms.assets
    ########################################################################
