from Manager.DataManager import *


class PortfolioManager:
    def __init__(self, param):
        self.param = param
        self.dm = DataManager(param)
    @L2
    def experiment(self):
        self.dm.prepare_data()
