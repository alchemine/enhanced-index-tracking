from Engine.CPU.fitness_grocery import *

### Datatype ####################################################
Asset   = lambda *shape: np.zeros(shape, dtype=np.uint8)
Weight  = lambda *shape: np.zeros(shape, dtype=np.float32)
Fitness = lambda NP: np.zeros(NP, dtype=np.float32)
#################################################################


class Portfolio:
    def __init__(self, data, param, shape, weight_init_method='cap'):
        self.data  = data
        self.param = param
        self.weight_init_method = weight_init_method
        self.id: str

        self.assets    = Asset(*shape)
        self.weights   = Weight(*shape)
        self.fitnesses = Fitness(shape[0])

        self._initialize()
    def __repr__(self):
        NP, NA = self.assets.shape
        s = f"[# portfolio: {NP}, # asset: {NA}] \n"
        n_pf = 3 if NP >= 6 else NP // 2
        for idx_pf in list(range(n_pf)) + list(range(NP-n_pf, NP)):
            s += f"{idx_pf}: %s \n" % str({a: round(w, 2) for a, w in zip(self.assets[idx_pf], self.weights[idx_pf])})
        return s


    ### Public method ###########################################
    def get(self):
        return self.assets, self.weights, self.fitnesses
    # @L
    def evaluate(self, update_weight=True):
        if update_weight:
            self._update_weights(self.weight_init_method)
        fn = get_fitness_fn(self.data, self.param)
        fn(self.fitnesses, self.assets, self.weights)
    def select_top(self, n):
        order = -1 if self.param['maximize_fitness'] else 1
        self.select(np.argsort(self.fitnesses)[::order][:n])
    def select(self, idxs):
        self.assets    = self.assets[idxs]
        self.weights   = self.weights[idxs]
        self.fitnesses = self.fitnesses[idxs]
    def update(self, pf):
        self.assets    = pf.assets
        self.weights   = pf.weights
        self.fitnesses = pf.fitnesses
    #############################################################


    ''
    ### Private method ##########################################
    def _initialize(self):
        self._generate_assets()
        self.evaluate()
    @L
    def _generate_assets(self):
        @njit(parallel=True)  # n_pop: 2^24 -> 74.42s (parallel=True: 7.76s)
        def fn(assets, n_asset_src):
            n_pop, n_asset_pop = assets.shape
            for idx_chrom in prange(n_pop):
                assets[idx_chrom] = np.random.choice(n_asset_src, n_asset_pop, replace=False)
        fn(self.assets, self.param['N'])
    def _update_weights(self, method):
        if method == 'cap':
            @njit  # n_pop: 2^24 -> 5.39s (parallel=True: 10.04s)
            def fn(weights, assets, caps):
                for idx_pf in range(len(weights)):
                    weights[idx_pf] = NORMALIZE(caps[assets[idx_pf]])
            fn(self.weights, self.assets, self.data['cap'][-1])
        else:
            raise ValueError(f"Unknown method: {method}")
    #############################################################


class GAPortfolio(Portfolio):
    def __init__(self, data, param):
        super().__init__(data, param, (param['n_pop_GA'], param['K']), param['weight_init_method_GA'])


class EVPortfolio(Portfolio):
    def __init__(self, data, param, pf):
        self.pf = pf
        super().__init__(data, param, (param['n_pop_EV'], param['K']), param['weight_init_method_EV'])
    def _initialize(self):
        n_island = self.param['n_pop_EV'] // self.param['n_pop_GA']
        self.islands = np.array([(s, s+n_island) for s in range(0, self.param['n_pop_EV'], n_island)])
        for idx_island, (s, e) in enumerate(self.islands):
            self.assets[s:e]  = self.pf.assets[idx_island]
            self.weights[s:e] = self.pf.weights[idx_island]
        self.evaluate()
    def _update_weights(self, method):
        if method == 'weighted':
            @njit  # (1.45s -> 0.65s / 1.08s)
            def fn(weights, thr):
                for idx_pf in range(len(weights)):
                    rnds = 1 - (2*thr)*np.random.rand(len(weights[idx_pf])) - thr
                    weights[idx_pf] = NORMALIZE(weights[idx_pf]*rnds)
            fn(self.weights, self.param['weight_init_threshold_EV'])
        elif method == 'random':
            @njit
            def fn(weights):
                for idx_pf in range(len(weights)):
                    weights[idx_pf] = NORMALIZE(np.random.rand(len(weights[idx_pf])))
            fn(self.weights)
        else:
            raise ValueError(f"Unknown method: {method}")
