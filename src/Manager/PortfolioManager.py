from Manager.DataManager import *
from Engine.Engine import *


class PortfolioManager:
    def __init__(self, param):
        self.param  = param
        self.dm     = DataManager(param)
        self.engine = Engine(self.dm, param)

    @L1
    def experiment(self):
        ### 1. Prepare data
        self.dm.prepare_data()

        self.param['cur_date'] = self.param['start_date']
        while self.param['cur_date'] <= self.param['end_date']:
            ### 2. Train
            self.engine.train()

            ### 3. Test
            self.engine.test()
            break