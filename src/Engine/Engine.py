from Engine.Portfolio import *
from Engine.GeneticSolver import *


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
        pf = self._get_base_portfolio()

        ## 2. Select portfolios
        pfs = self._select_candidate_portfolios(pf)

    @L
    def _get_base_portfolio(self):
        ## Weight is initialized with the latest cap
        return Portfolio(assets=[range(self.param['N'])], weights=Weight([self.data['cap'][-1]]))
    @L
    def _select_candidate_portfolios(self, pf):
        ## 1. Random sampling
        pfs = self._generate_population()

        ## 2. Genetic algorithm
        # geneticSolver = GeneticSolver(self.data, self.param)
        # pfs = geneticSolver.run(pop)
    @L
    def _generate_population(self):
        assets  = self._generate_assets(shape=(self.param['n_pop_GA'], self.param['K']), n_asset_src=self.param['N'])
        weights = self._generate_weights(assets, self.data['cap'][-1])

    @staticmethod
    @L
    @njit(parallel=True)  # n_pop: 2^24 -> 74.42s (parallel=True: 7.76s)
    def _generate_assets(shape, n_asset_src):
        n_pop, n_asset_pop = shape
        assets = np.empty(shape, dtype=np.uint8)  # np.zeros() occurs error
        for idx_chrom in prange(n_pop):
            assets[idx_chrom] = np.random.choice(n_asset_src, n_asset_pop, replace=False)
        return assets
    @staticmethod
    @L
    @njit  # n_pop: 2^24 -> 5.39s (parallel=True: 10.04s)
    def _generate_weights(assets, caps):
        weights = np.zeros_like(assets, dtype=np.float32)
        for idx_chrom in range(len(weights)):
            weights[idx_chrom] = NORMALIZE(caps[assets[idx_chrom]])
        return weights
    ########################################################################
