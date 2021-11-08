from Engine.util import *


class Portfolio:
    def __init__(self, assets, weights):
        self.assets  = Asset(assets)
        self.weights = Weight(weights)
