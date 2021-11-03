from Env.util import *
from Logger.Logger import *
from Controller.Controller import *


class Interface:
    def __init__(self):
        self.logger = Logger(PATH.LOG)
        self.controller = Controller()

    @L1
    def run(self, CMD, **param):
        tprint(param)
        if CMD == "save_data":
            self.controller.save_data(param)
        else:
            raise NotImplementedError

