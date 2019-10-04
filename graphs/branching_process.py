from graphs.graph import Graph
import functools
import numpy as np


class BranchingProcess(Graph):
    @staticmethod
    def generate_binomial_function(n, p):
        return functools.partial(np.random.binomial, n=n, p=p)

    def __init__(self, max_generation, distribution):
        V = [Graph.Node(None)]
        E = set()
        self.generations = [1]
        self.t = 0
        gen_size = 1
        sum_of_previous_generations = 0
        while (self.t < max_generation or gen_size == 0):
            new_gen_size = 0
            for i in range(gen_size):
                num_children = distribution()
                for j in range(num_children):
                    V.append(Graph.Node(None))
                    E.add((sum_of_previous_generations + i, sum_of_previous_generations + gen_size + new_gen_size + j))
                new_gen_size += num_children

            sum_of_previous_generations += gen_size
            gen_size = new_gen_size
            self.generations.append(new_gen_size)
            self.t += 1
        super(BranchingProcess, self).__init__(V, E)

    def generate_layout(self, max_nbs=0):
        sum_of_previous_generations = 0
        for i in range(len(self.generations)):
            gen_size = self.generations[i]
            offset = int(gen_size / 2)
            for j in range(gen_size):
                self.V[sum_of_previous_generations + j].pos = (j - offset, i)
            sum_of_previous_generations += gen_size
