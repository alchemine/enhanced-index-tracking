from Env.util import *


class Controller:
    @L2
    def invest(self, param):
        full_dates = get_dates(param['start_date'], param['end_date'], param)
        print(full_dates)