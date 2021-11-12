from Engine.CPU.util import *


class Solver:
    def __init__(self, id, data, param):
        self.id    = id
        self.data  = data
        self.param = param

        ## Metrics
        self.opt_fitnesses: list
        self.avg_fitnesses: list
    def _update_fitness(self, fitnesses):
        self.opt_fitnesses.append(max(fitnesses) if self.param['maximize_fitness'] else min(fitnesses))
        self.avg_fitnesses.append(np.mean(fitnesses))
    def _plot_fitness(self):
        fig, ax = plt.subplots(figsize=(10, 5))
        X = 1+np.arange(len(self.opt_fitnesses))
        ax.plot(X, self.opt_fitnesses, label=f'Optimal Fitness({self.opt_fitnesses[-1]:.2e})')
        ax.plot(X, self.avg_fitnesses, label=f'Average Fitness({self.avg_fitnesses[-1]:.2e})')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Fitness')
        ax.legend();  ax.grid()
        ax.set_yscale('log')
        ax.set_title(f"{self.id} result")
        fig.show()
    def _replace(self, parents, childs):
        for idx_pf in range(len(parents.assets)):
            if (self.param['maximize_fitness'] and (parents.fitnesses[idx_pf] < childs.fitnesses[idx_pf])) or (not self.param['maximize_fitness'] and (parents.fitnesses[idx_pf] > childs.fitnesses[idx_pf])):
                parents.assets[idx_pf]    = childs.assets[idx_pf]
                parents.weights[idx_pf]   = childs.weights[idx_pf]
                parents.fitnesses[idx_pf] = childs.fitnesses[idx_pf]
