from graphs.graph import Graph
import numpy as np


class PA_Graph(Graph):
    class PA_Node(Graph.Node):
        def __init__(self, nbs, _id=-1, has_self_loop=False):
            super(PA_Graph.PA_Node, self).__init__(nbs, _id)
            self.self_loop = has_self_loop

        def degree(self):
            return len(self.nbs) + (2 if self.self_loop else 0)

    def __init__(self, _m=1, _d=0, t=1):
        self.m = _m
        self.d = _d
        super(PA_Graph, self).__init__([PA_Graph.PA_Node(None, i, True) for i in range(self.m)], set())
        for _ in range(t-1):
            self.evolve()

    def evolve(self):
        t = len(self.V) - self.m + 1
        nodes = len(self.V)
        new_node = PA_Graph.PA_Node(set(), nodes, np.random.uniform(0, 1) <= (1 + self.d) / (t * (2 + self.d) + (1 + self.d)))
        self.V.append(new_node)
        for i in range(nodes):
            v = self.V[i]
            if np.random.uniform(0,1) <= (v.degree()+self.d)/(t*(2+self.d) + (1+self.d)):
                self.E.add((i, nodes))
                self.edgelist.append((i,nodes))
                v.nbs.add(new_node)
                new_node.nbs.add(v)