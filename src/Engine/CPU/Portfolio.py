from Engine.CPU.util import *


### Datatype ####################################################
Asset  = lambda data: np.array(data, dtype=np.uint8)
Weight = lambda data: np.array(data, dtype=np.float16)
#################################################################


class Portfolio:
    def __init__(self, assets, weights):
        self.assets  = Asset(assets)
        self.weights = Weight(weights)
    def __repr__(self):
        n = len(self.assets)
        for idx_pf in [0, 1, 2, n-3, n-2, n-1]:
            print(f"{idx_pf}:", {a: round(w, 2) for a, w in zip(self.assets[idx_pf], self.weights[idx_pf])})
        return ""
