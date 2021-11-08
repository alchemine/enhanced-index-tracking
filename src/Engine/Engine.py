from Env.util import *


class Engine:
    def __init__(self, dm, param):
        self.dm = dm
        self.param = param


    ### Public method ######################################################
    @L2
    def train(self):
        ### 1. Preprocess data
        self.data = self._process_data()
    @L2
    def test(self):
        pass
    ########################################################################


    ''
    ### Private method #####################################################
    @L3
    def _process_data(self):
        return self.dm.select_universe()
    ########################################################################