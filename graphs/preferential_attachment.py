from graphs.graph import Graph
import numpy as np


class PA_Graph(Graph):
    class PA_Node(Graph.Node):
        def __init__(self, nbs: dict, _id=-1, has_self_loop=False):
            super(PA_Graph.PA_Node, self).__init__(nbs, _id)
            self.self_loop = has_self_loop

        def degree(self):
            return len(self.nbs) + (2 if self.self_loop else 0)

    def __init__(self, _m=1, _d=0, t=1):
        self.m = _m
        self.d = _d
        super(PA_Graph, self).__init__([PA_Graph.PA_Node(None, 0, True)], set())
        if (self.m == 1):
            for _ in range(t-1):
                self.evolve()
        else:
            for _ in range(self.m*t-1):
                self.evolve()
            new_V, new_E = self.collapse()
            super(PA_Graph, self).__init__(new_V, new_E)


    def evolve(self):
        t = len(self.V) + 1
        nodes = len(self.V)
        new_node = PA_Graph.PA_Node(set(), nodes, np.random.uniform(0, 1) <= (1 + self.d) / (t * (2 + self.d) + (1 + self.d)))
        self.V.append(new_node)
        for i in range(nodes):
            v = self.V[i]
            factor = self.d/self.m
            if np.random.uniform(0,1) <= (v.degree()+factor)/(t*(2+factor) + (1+factor)):
                self.E.add((i, nodes))
                self.edgelist.append((i,nodes))
                v.nbs.add(new_node)
                new_node.nbs.add(v)

    def collapse(self):
        new_V = []
        new_E = set()
        t = len(self.V)//self.m
        for i in range(0, self.m * t, self.m):
            new_node = PA_Graph.PA_Node(None, len(new_V), False)
            for j in range(self.m):
                if self.V[i + j].self_loop:
                    new_node.self_loop = True
            new_V.append(new_node)
        for (a, b) in self.E:
            a2 = a // self.m
            b2 = b // self.m
            if a2 == b2:
                new_V[a2].self_loop = True
            else:
                new_E.add((a2, b2))
        return new_V, new_E