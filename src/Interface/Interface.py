from Env.util import *
from Controller.Controller import *


class Interface:
    def __init__(self):
        self.controller = Controller()

    @L1
    def run(self, cmd, **param):
        tprint(param)
        with Switch(cmd) as case:
            if case('invest'):
                self.controller.invest(param)
            if case.default:
                raise ValueError(f'Invalid CMD: {cmd}')
