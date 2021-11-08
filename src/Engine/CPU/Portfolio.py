from Engine.CPU.fitness_grocery import *


### Datatype ####################################################
Asset  = lambda data: np.array(data, dtype=np.uint8)
Weight = lambda data: np.array(data, dtype=np.float16)
#################################################################


class Portfolio:
    def __init__(self, assets, weights, data, param):
        self.assets    = Asset(assets)
        self.weights   = Weight(weights)
        self.fitnesses = np.zeros_like(self.assets, dtype=np.float16)

        self.fitness_fn = get_fitness_fn(data, param)
    def __repr__(self):
        s = ""
        n = len(self.assets)
        for idx_pf in [0, 1, 2, n-3, n-2, n-1]:
            s += f"{idx_pf}: %s \n" % str({a: round(w, 2) for a, w in zip(self.assets[idx_pf], self.weights[idx_pf])})
        return s
