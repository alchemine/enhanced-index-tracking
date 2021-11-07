from Env.util import *


class Engine:
    def __init__(self, dm, param):
        self.dm = dm
        self.param = param


    @L2
    def train(self):
        ### 1. Preprocess data
        self.data = self.process_data()


    @L2
    def test(self):
        pass

    @L3
    def process_data(self):
        return self.dm.select_universe()
