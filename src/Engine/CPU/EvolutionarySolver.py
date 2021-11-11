from Engine.CPU.Solver import *
from Engine.CPU.Portfolio import *


class EvolutionarySolver(Solver):
    def __init__(self, data, param):
        super().__init__("EV")
        self.data  = data
        self.param = param

        self.parents: Portfolio
        self.childs:  Portfolio
        self.mutants: Portfolio
        self.trials:  Portfolio

        ## Metrics
        self.opt_fitnesses = []
        self.avg_fitnesses = []

    ### Public method ######################################################
    def run(self, parents):
        self.parents = parents
        self.childs  = EVPortfolio(self.data, self.param, parents)
        self.mutants = EVPortfolio(self.data, self.param, parents)
        self.trials  = EVPortfolio(self.data, self.param, parents)

        for idx_iter in tqdm(range(self.param['max_iter_EV'])):
            ## 1. Mutation
            self._mutate(self.childs.weights, self.mutants.weights, self.childs.islands, self.param['F'])

            ## 2. Recombination
            self._recombinate(self.childs.weights, self.mutants.weights, self.trials.weights)

            ## 3. Replace
            self.trials.evaluate(update_weight=False)
            self._replace(self.childs, self.trials, self.param['maximize_fitness'])

            ## Update fitnesses
            self._update_fitness(self.childs.fitnesses)

        ## 4. Select optimal weights
        self._select()
        self._plot_fitness()
    ########################################################################


    ''
    ### Private method #####################################################
    def _select(self):
        """Select top n_candidate chromosome"""
        self.childs.select_top(len(self.parents.weights))
        self.parents.update(self.childs)
    @staticmethod
    @njit  # (2.36s -> 0.34s / error)
    def _recombinate(pop, mutants, trials):
        rnds = np.random.rand(*trials.shape)
        idx_asset_mutant = np.random.choice(pop.shape[1])

        for idx_pf in range(len(pop)):
            for idx_asset in range(len(pop[idx_pf])):
                if rnds[idx_pf, idx_asset] < 0.5 or idx_asset == idx_asset_mutant:
                    trials[idx_pf, idx_asset] = mutants[idx_pf, idx_asset]
                else:
                    trials[idx_pf, idx_asset] = pop[idx_pf, idx_asset]
            NORMALIZE(trials[idx_pf])
    @staticmethod
    # @njit  # (0.40s -> 0.47s / 1.09s)
    def _mutate(pop, mutants, islands, F):
        ## w1, w2, w3 <- randomly selected weights
        ## mutant <- w1 + f(w2 - w3)

        for s, e in islands:
            parents      = pop[s:e]
            w1, w2, w3   = parents[np.random.choice(e-s, 3, replace=False)]
            mutants[s:e] = w1 + F * (w2 - w3)
            NORMALIZE(mutants[s:e])
    ########################################################################
