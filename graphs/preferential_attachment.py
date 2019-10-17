from graphs.graph import MultiGraph
import numpy as np


class PA_Graph(MultiGraph):

    def __init__(self, _m=1, _d=0, t=1):
        self.m = _m
        self.d = _d
        self.distribution = [0, 0]
        e = dict()
        e[(0, 0)] = 1
        super(PA_Graph, self).__init__([PA_Graph.MultiNode(dict(), 0)], e)
        if (self.m == 1):
            for _ in range(t - 1):
                self.evolve()
            self.edgelist = [(i, j, k) for ((i,j), k) in self.E.items()]
        else:
            for _ in range(self.m * t - 1):
                self.evolve()
            new_V, new_E = self.collapse()
            super(PA_Graph, self).__init__(new_V, new_E)
        print()

    def evolve(self):
        t = len(self.V) + 1
        nodes = len(self.V)
        new_node = PA_Graph.MultiNode(dict(), nodes)
        self.V.append(new_node)
        self.distribution.append(nodes)
        p = [2 * t + 1, 2 * self.d]
        if np.random.uniform(0, sum(p)) <= p[0]:
            r = np.random.choice(self.distribution)
        else:
            r = np.random.choice(self.V).id
        self.E[(r, nodes)] = 1
        new_node.add_nb(self.V[r])
        self.V[r].add_nb(new_node)
        self.distribution.append(r)

    def collapse(self):
        new_V = []
        new_E = dict()
        t = len(self.V) // self.m
        for i in range(0, self.m * t, self.m):
            new_node = PA_Graph.MultiNode(None, len(new_V))
            new_V.append(new_node)
        for (a, b) in self.E:
            a2 = a // self.m
            b2 = b // self.m
            new_E[(a2, b2)] = 1
        return new_V, new_E
