from Engine.CPU.Portfolio import *
from Engine.CPU.GeneticSolver import *


class Engine:
    def __init__(self, dm, param):
        self.dm    = dm
        self.param = param
        self.data  = dict()

        ## Set random seed
        np.random.seed(self.param['seed'])
    ### Public method ######################################################
    @L
    def train(self):
        ## 1. Preprocess data
        self._process_data_param()

        ## 2. Generate portfolios
        pf = self._select_optimal_portfolio()

    @L
    def test(self):
        pass
    ########################################################################


    ''
    ### Private method #####################################################
    @L
    def _process_data_param(self):
        ## 1. Select universe
        self.data = self.dm.select_universe()

        ## 2. Parameter
        self._get_processed_param()
    def _get_processed_param(self):
        self.param['T'], self.param['N'] = self.data['stock_price'].shape
    @L
    def _select_optimal_portfolio(self):
        ## 1. Initialize portfolio with cap weight
        base_pf = Portfolio(self.data, self.param, shape=(1, self.param['N']))

        ## 2. Select portfolios
        pfs = self._select_candidate_portfolios()

        # ## 3. Filter portfolios
        # return self._filter_candidates(pfs)

    @L
    def _select_candidate_portfolios(self):
        ## 1. Random sampling
        base_pf = Portfolio(self.data, self.param, shape=(self.param['n_pop_GA'], self.param['K']))

        ## 2. Genetic-Evolutionary algorithm
        geneticSolver = GeneticSolver(self.data, self.param)
        return geneticSolver.run(base_pf)
    # @L
    # def _filter_candidates(self, pfs):
    ########################################################################
