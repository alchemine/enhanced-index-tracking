from Engine.util import *


class Solver:
    def __init__(self, id):
        self.id = id

    def _obj(self, chrom):  # input: chromosome(portfolio)
        return 1