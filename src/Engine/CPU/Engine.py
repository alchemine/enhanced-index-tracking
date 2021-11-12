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
        self._process_data_param('train')

        ## 2. Generate portfolios
        base    = Portfolio(self.data, self.param, shape=(1, self.param['N']))
        optimal = self._select_optimal_portfolio()

        ## 3. Plot result
        self._plot_result_train(base, optimal)
        self.param['cur_date'] = self.dm.get_date_from_date(self.param['cur_date'], self.param['train_days'])
        results = dict(base=base.to_dict(), optimal=optimal.to_dict(), data=self.data, param=self.param)
        return results
    @L
    def test(self, train_results):
        test_results = dict(base_price=[], optimal_price=[], index_price=[])

        ## 1. Preprocess data
        self._process_data_param('test')

        for idx_test_day in tqdm(range(self.param['test_days'])):
            ## 2. Invest
            self._invest(train_results, test_results, idx_test_day)
            self.param['cur_date'] = self.dm.get_date_from_date(self.param['cur_date'], 1)

            ## 3. check rebalancing condition
            if self._rebalancing_condition(test_results):
                for key in (k for k in self.data if k not in ['asset', 'index_name']):
                    self.data[key] = self.data[key][:idx_test_day+1]
                break

        ## 4. Plot result
        self._plot_result_test(*test_results.values())
    ########################################################################


    ''
    ### Private method #####################################################
    @L
    def _process_data_param(self, cmd):
        ## 1. Select universe
        universe_date = 'end_date' if cmd == 'train' else self.dm.get_date_from_date(self.param['cur_date'], -1)
        self.data = self.dm.select_universe(start_date=self.param['cur_date'],
                                            end_date=self.dm.get_date_from_date(self.param['cur_date'], self.param[f'{cmd}_days']-1),
                                            universe_date=universe_date)

        ## 2. Parameter
        self._get_processed_param()
    def _get_processed_param(self):
        self.param['T'], self.param['N'] = self.data['stock_price'].shape
    @L
    def _select_optimal_portfolio(self):
        ## 2. Select portfolios
        candidates = self._select_candidate_portfolios()

        ## 3. Filter portfolios
        optimal = self._filter_candidates(candidates)
        return optimal
    def _select_candidate_portfolios(self):
        ## Genetic-Evolutionary algorithm
        geneticSolver = GeneticSolver(self.data, self.param)
        return geneticSolver.run()
    def _filter_candidates(self, pfs):
        optimal_idx = filter(self.data, self.param, pfs)
        pfs.select(optimal_idx)
        return pfs
    def _plot_result_train(self, base, optimal):
        base_prices, base_returns       = get_pf_prices_returns(base.assets, base.weights, self.data['stock_price'])
        optimal_prices, optimal_returns = get_pf_prices_returns(optimal.assets, optimal.weights, self.data['stock_price'])
        index_prices, index_returns     = self.data['index_price'], self.data['index_return']

        fig, axes = plt.subplots(2, 1, figsize=(16, 8))
        dates = pd.to_datetime(self.data['date'])

        ## 1. Price
        index_prices = pd.DataFrame({self.data['index_name']: index_prices/index_prices[0]}, index=dates)
        pf_prices    = pd.DataFrame({'base': base_prices[0], 'optimal': optimal_prices[0]}, index=dates)
        index_prices.plot(ax=axes[0], color='k', linewidth=2)
        pf_prices.plot(ax=axes[0], linewidth=2)

        ## 2. Ratio
        pf_ratios = pf_prices / index_prices.values
        pf_ratios.plot(ax=axes[1], linewidth=2)
        axes[1].axhline(1, color='k', linewidth=2)

        ## 3. Options
        for ax in axes:
            ax.grid();  ax.legend()

        axes[0].set_title(f"Portfolio result in Training set({self.data['date'][0]}~{self.data['date'][-1]})")
        axes[0].set_ylabel('Price (normalized)')
        axes[1].set_ylabel('Price / Index')
        axes[0].set_xticklabels([])

        fig.set_tight_layout(True)
        fig.show()
    def _plot_result_test(self, base_prices, optimal_prices, index_prices):
        fig, axes = plt.subplots(2, 1, figsize=(16, 8))
        dates = pd.to_datetime(self.data['date'])

        ## 1. Price
        index_prices = pd.DataFrame({self.data['index_name']: index_prices/index_prices[0]}, index=dates)
        pf_prices    = pd.DataFrame({'base': base_prices/base_prices[0], 'optimal': optimal_prices/optimal_prices[0]}, index=dates)
        index_prices.plot(ax=axes[0], color='k', linewidth=2)
        pf_prices.plot(ax=axes[0], linewidth=2)

        ## 2. Ratio
        pf_ratios = pf_prices / index_prices.values
        pf_ratios.plot(ax=axes[1], linewidth=2)
        axes[1].axhline(1, color='k', linewidth=2)

        ## 3. Options
        for ax in axes:
            ax.grid();  ax.legend()

        axes[0].set_title(f"Portfolio result in Test set({self.data['date'][0]}~{self.data['date'][-1]})")
        axes[0].set_ylabel('Price (normalized)')
        axes[1].set_ylabel('Price / Index')
        axes[0].set_xticklabels([])

        fig.set_tight_layout(True)
        fig.show()
    def _invest(self, train_results, test_results, idx_test_day):
        base, optimal = train_results['base'], train_results['optimal']

        base_prices, _    = get_pf_prices_returns(base['assets'], base['weights'], self.data['stock_price'][[idx_test_day]], normalize=False)
        optimal_prices, _ = get_pf_prices_returns(optimal['assets'], optimal['weights'], self.data['stock_price'][[idx_test_day]], normalize=False)
        index_prices      = self.data['index_price'][[idx_test_day]]

        for key, val in zip(['base_price', 'optimal_price', 'index_price'], [base_prices[0][0], optimal_prices[0][0], index_prices[0]]):
            test_results[key].append(val)
    def _rebalancing_condition(self, test_results):
        optimal_prices = test_results['optimal_price']
        if optimal_prices[-1]/optimal_prices[0] - 1 < self.param['rebalancing_return_threshold']:
            return True
        return False
    ########################################################################
