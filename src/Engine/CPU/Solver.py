from Engine.CPU.util import *


class Solver:
    def __init__(self, id):
        self.id = id

        ## Metrics
        self.opt_fitness = []
        self.avg_fitness = []
