from Manager.PortfolioManager import *


class Interface:
    def run(self, cmd, **param):
        tprint(param)

        self.pm = PortfolioManager(param)
        with Switch(cmd) as case:
            if case('experiment'):
                self.pm.experiment()
            if case.default:
                raise ValueError(f'Invalid command: {cmd}')
