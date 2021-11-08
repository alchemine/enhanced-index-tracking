from Engine.Portfolio import *


class Engine:
    def __init__(self, dm, param):
        self.dm    = dm
        self.param = copy(param)
        self.data  = dict()

    ### Public method ######################################################
    @L2
    def train(self):
        ## 1. Preprocess data
        self._process_data_param()

        ## 2. Generate portfolios
        pf = self._select_optimal_portfolio()

    @L2
    def test(self):
        pass
    ########################################################################


    ''
    ### Private method #####################################################
    @L3
    def _process_data_param(self):
        ## 1. Select universe
        self.data = self.dm.select_universe()

        ## 2. Parameter
        self.param = self._get_processed_param()
    @L4
    def _get_processed_param(self):
        param = {}
        param['T'], param['N'] = self.data['stock_price'].shape
        return param
    @L3
    def _select_optimal_portfolio(self):
        ## 1. Initialize portfolio with cap weight
        pf = self._initialize_portfolio()

        ## 2. Select portfolios
        pfs = self._select_candidate_portfolios(pf)

    @L4
    def _initialize_portfolio(self):
        ## Weight is initialized with the latest cap
        return Portfolio(assets=[range(self.param['N'])], weights=NORMALIZE(Weight([self.data['cap'][-1]])))
    @L4
    def _select_candidate_portfolios(self, pf):
        pass
    ########################################################################
