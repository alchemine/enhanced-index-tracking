from Env.util import *


class DataManager:
    def __init__(self, param):
        self.param = param
    def prepare_data(self):
        full_dates = get_dates(self.param['start_date'], self.param['end_date'], self.param)
        print(full_dates)