from graphs.graph import Graph, MinimalistGraph
import numpy as np
import random


class GRG(Graph):
    def __init__(self, _w: iter):
        self.w = sorted(_w)
        n = len(self.w)
        ln = sum(self.w)
        V = []
        for i in range(n):
            newnode = Graph.Node(set(), i)
            newnode.w = self.w[i]
            V.append(newnode)
        E = set([(i, j) for i in range(n) for j in range(i+1, n) if
                 random.uniform(0., 1.) < (self.w[i] * self.w[j]) / (ln + self.w[i] * self.w[j])])
        super(GRG, self).__init__(V, E)

    @staticmethod
    def from_distribution(f, n):
        return GRG([f() for _ in range(n)])

def GRG_degrees(w):
    # Assume w sorted
    d = np.zeros(len(w), dtype=np.int)
    n = len(w)
    ln = sum(w)
    edgelist = [(i, j) for i in range(n) for j in range(i + 1, n) if random.uniform(0., 1.) < (w[i] * w[j]) / (ln + w[i] * w[j])]
    for (i,j) in edgelist:
        d[i] += 1
        d[j] += 1
    return d
