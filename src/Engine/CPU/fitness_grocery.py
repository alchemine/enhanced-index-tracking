from Engine.CPU.util import *


def get_fitness_fn(data, param):
    ## Constants
    T            = param['T']
    stock_prices = data['stock_price']
    index_return = data['index_return']

    ## Functions
    def get_pf_prices_returns(assets, weights):
        pf_prices  = np.zeros((len(assets), T), dtype=np.float32)
        pf_returns = np.zeros((len(assets), T), dtype=np.float32)
        compute_pf_prices(pf_prices, assets, weights)
        compute_pf_returns(pf_prices, pf_returns)
        return pf_prices, pf_returns
    @njit(parallel=True)
    def compute_pf_prices(pf_prices, assets, weights):
        for idx_pf in prange(len(pf_prices)):
            pf_prices[idx_pf] = stock_prices[:, assets[idx_pf]] @ weights[idx_pf]  # [T, K] @ [K] -> [T]
            pf_prices[idx_pf] /= pf_prices[idx_pf, 0]  # Set start value to 1
    @njit(parallel=True)
    def compute_pf_returns(pf_prices, pf_returns):
        for idx_pf in prange(len(pf_returns)):
            for t in prange(1, T):  # [0] is initialized with 0
                pf_returns[idx_pf, t] = pf_prices[idx_pf, t] / pf_prices[idx_pf, 0] - 1


    ## Selection
    with Switch(param['fitness_fn']) as case:
        if case('downside_risk'):
            def fn(fitnesses, assets, weights):
                pf_prices, pf_returns = get_pf_prices_returns(assets, weights)
                for idx_pf, pf_return in enumerate(zip(pf_returns)):
                    downside_return = np.where(pf_return > index_return, 0, pf_return - index_return)
                    fitnesses[idx_pf] = np.sqrt(np.mean(downside_return**2))
    return fn
