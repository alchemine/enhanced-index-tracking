from Engine.CPU.util import *


class Solver:
    def __init__(self, id):
        self.id = id

        ## Metrics
        self.opt_fitnesses: list
        self.avg_fitnesses: list
    def _update_fitness(self, fitnesses):
        self.opt_fitnesses.append(fitnesses[0])
        self.avg_fitnesses.append(np.mean(fitnesses))
    def _plot_fitness(self):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.opt_fitnesses, label=f'Optimal Fitness({self.opt_fitnesses[-1]:.3f})')
        ax.plot(self.avg_fitnesses, label=f'Average Fitness({self.avg_fitnesses[-1]:.3f})')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Fitness')
        ax.legend();  ax.grid()
        ax.set_title(f"{self.id} result")
        fig.show()
    def _replace(self, parents, childs, maximize_fitness):
        for idx_pf in range(len(parents.assets)):
            if (maximize_fitness and (parents.fitnesses[idx_pf] < childs.fitnesses[idx_pf])) or (not maximize_fitness and (parents.fitnesses[idx_pf] > childs.fitnesses[idx_pf])):
                parents.assets[idx_pf]    = childs.assets[idx_pf]
                parents.weights[idx_pf]   = childs.weights[idx_pf]
                parents.fitnesses[idx_pf] = childs.fitnesses[idx_pf]
