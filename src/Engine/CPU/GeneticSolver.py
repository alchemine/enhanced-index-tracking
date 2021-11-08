from Engine.CPU.Solver import *
from sko.GA import GA


class GeneticSolver(Solver):
    def __init__(self, data, param):
        super().__init__("GA")
        self.data  = data
        self.param = param

    ### Public method ######################################################
    @L
    def run(self, pf):
        ## 1. Initialize GA model
        model = self._get_initialized_model()

    ########################################################################


    ''
    ### Private method #####################################################
    def _get_initialized_model(self):
        model = GA(func=self._obj,
                   n_dim=self.param['K'],
                   size_pop=self.param['n_pop_GA'],
                   max_iter=self.param['max_iter_GA'])
        return model
    ########################################################################

