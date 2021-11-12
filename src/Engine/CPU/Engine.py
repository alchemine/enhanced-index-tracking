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
        optimal = self._select_optimal_portfolio()
        print(optimal)


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
        base = Portfolio(self.data, self.param, shape=(1, self.param['N']))

        ## 2. Select portfolios
        candidates = self._select_candidate_portfolios()

        ## 3. Filter portfolios
        optimal = self._filter_candidates(candidates)
        return optimal

    @L
    def _select_candidate_portfolios(self):
        ## Genetic-Evolutionary algorithm
        geneticSolver = GeneticSolver(self.data, self.param)
        return geneticSolver.run()

    def _filter_candidates(self, pfs):
        optimal_idx = filter(self.data, self.param, pfs)
        pfs.select(optimal_idx)
        return pfs
    ########################################################################
