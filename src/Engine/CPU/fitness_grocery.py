from Engine.CPU.util import *


def get_fitness_fn(data, param):
    with Switch(param['fitness_fn']) as case:
        if case('downside_risk'):
            def fn(*assets):
                return sum(assets)
    return fn
