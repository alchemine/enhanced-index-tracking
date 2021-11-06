from Manager.DataManager import *


class PortfolioManager:
    def __init__(self, param):
        self.param = param
    @L2
    def experiment(self):
        self.prepare_data()

    def prepare_data(self):
        full_dates = get_dates(self.param['start_date'], self.param['end_date'], self.param)

