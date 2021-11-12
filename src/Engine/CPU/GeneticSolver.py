from Engine.CPU.EvolutionarySolver import *


class GeneticSolver(Solver):
    def __init__(self, data, param):
        super().__init__("GA", data, param)
        self.data  = data
        self.param = param

        ## Metrics
        self.opt_fitnesses = []
        self.avg_fitnesses = []

        ## 1. Initialization
        self.parents = Portfolio(self.data, self.param, shape=(self.param['n_pop_GA'], self.param['K']))  # n_pop_GA
        self.childs  = GAPortfolio(self.data, self.param)  # NP: n_pop_GA

        self.evolutionarySolver = EvolutionarySolver(self.data, self.param)


    ### Public method ######################################################
    @L
    def run(self):
        for idx_iter in tqdm(range(self.param['max_iter_GA'])):
            ## 1. Recombination
            self._recombinate(self.parents.assets, self.childs.assets)

            ## 2. Mutation
            self._mutate(self.childs.assets, self.param['mutation_rate_GA'], self.param['N'])

            ## 3. Find optimal weights for selected assets
            self.evolutionarySolver.run(self.childs)

            ## 4. Replace
            self._replace(self.parents, self.childs)

            self._update_fitness(self.childs.fitnesses)
        self._plot_fitness()

        ## 5. Select candidates
        self._select()

        return self.childs
    ########################################################################


    ''
    ### Private method #####################################################
    def _select(self):
        """Select top n_candidate chromosome"""
        self.parents.select_top(self.param['n_candidate_GA'])
        self.childs = self.parents
    @staticmethod
    @njit  # (2.49s -> 0.77s / 1.05s)
    def _recombinate(parents, childs):
        NP, K = childs.shape
        for idx_pf in range(len(childs)):
            idx_parent1, idx_parent2 = np.random.choice(len(parents), 2, replace=False)
            bags = np.append(parents[idx_parent1], parents[idx_parent2])  # already random

            for i in range(K):
                while True:
                    asset = np.random.choice(bags)
                    if asset in childs[idx_pf]:
                        break
                    else:
                        childs[idx_pf, i] = asset
                        break
    @staticmethod
    # @njit  # (0.81s -> 0.50s / 1.46s)
    def _mutate(childs, mutation_rate, N):
        NP, K = childs.shape
        for child in childs:
            rnds = np.random.random(K)
            idxs, = np.where(rnds < mutation_rate)  # mutation asset indices
            child[idxs] = np.random.choice(np.delete(np.arange(N), child), len(idxs), replace=False)
    ########################################################################
