from Manager.PortfolioManager import *


class Interface:
    def run(self, cmd, debug, **param):
        if debug:
            self._update_debug_mode_param(param)
        tprint(param)

        self.pm = PortfolioManager(param)
        with Switch(cmd) as case:
            if case('experiment'):
                self.pm.experiment()
            if case.default:
                raise ValueError(f'Invalid command: {cmd}')
    def _update_debug_mode_param(self, param):
        param.update({'max_iter_GA': 2, 'max_iter_EV': 2,
                      'n_pop_GA': 2**4, 'n_pop_EV': 2**8,
                      'n_candidate_GA': 2**2})
