from Engine.CPU.fitness_grocery import *


### Datatype ####################################################
Asset   = lambda *shape: np.zeros(shape, dtype=np.uint8)
Weight  = lambda *shape: np.zeros(shape, dtype=np.float32)
Fitness = lambda NP: np.zeros(NP, dtype=np.float32)
#################################################################


class Portfolio:
    def __init__(self, data, param, shape, init=True):
        self.data  = data
        self.param = param

        self.assets    = Asset(*shape)
        self.weights   = Weight(*shape)
        self.fitnesses = Fitness(shape[0])

        if init:
            self._initialize()
    def __repr__(self):
        s = ""
        n = len(self.assets)
        for idx_pf in [0, 1, 2, n-3, n-2, n-1]:
            s += f"{idx_pf}: %s \n" % str({a: round(w, 2) for a, w in zip(self.assets[idx_pf], self.weights[idx_pf])})
        return s


    ### Public method ###########################################
    def get(self):
        return self.assets, self.weights, self.fitnesses
    @L
    def evaluate(self):
        self._generate_weights()
        fn = get_fitness_fn(self.data, self.param)
        fn(self.fitnesses, self.assets, self.weights)
    @L
    def select_top(self, n):
        order = -1 if self.param['maximize_fitness'] else 1
        self.select(np.argsort(self.fitnesses)[::order][:n])
    def select(self, idxs):
        self.assets    = self.assets[idxs]
        self.weights   = self.weights[idxs]
        self.fitnesses = self.fitnesses[idxs]
    #############################################################


    ### Private method ##########################################
    @L
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
    @L
    def _generate_weights(self, method='cap'):
        if method == 'cap':
            @njit  # n_pop: 2^24 -> 5.39s (parallel=True: 10.04s)
            def fn(weights, assets, caps):
                for idx_chrom in range(len(weights)):
                    weights[idx_chrom] = NORMALIZE(caps[assets[idx_chrom]])
            fn(self.weights, self.assets, self.data['cap'][-1])
        else:
            raise ValuesError(f"Unknown method: {method}")
    #############################################################
