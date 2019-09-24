import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math
import numpy as np
import random

class Graph:

    class Node:
        def __init__(self, _nbs):
            self.nbs = _nbs
            if self.nbs is None:
                self.nbs = set()

    def __init__(self, _V : list, _E : set):
        self.V = _V
        self.E = _E
        self.build_neighbors()

    def build_neighbors(self):
        for e in self.E:
            self.V[e[0]].nbs.add(self.V[e[1]])
            self.V[e[1]].nbs.add(self.V[e[0]])

    def generate_layout(self):
        for v in self.V:
            v.pos = None
        self.V[0].pos = (0., 0.)
        max_x, min_x = self.recurse_layout(self.V[0], 0, math.tau)
        for i in range(len(self.V)):
            if self.V[i].pos == None:
                self.V[i].pos = (0, 0)
                max_x += 1
                max_x_tmp, min_x_tmp = self.recurse_layout(self.V[i], 0, math.tau)
                offset = max_x - min_x_tmp
                q = [self.V[i]]
                while len(q) > 0:
                    current = q.pop()
                    current.pos = (current.pos[0] + offset, current.pos[1])
                    for nb in current.nbs:
                        if nb.pos[0] <= max_x:
                            q.append(nb)
                max_x = max_x + max_x_tmp - min_x_tmp


    def recurse_layout(self, v, min_angle, max_angle):
        nodes = []
        max_x = 0
        min_x = 0
        for n in v.nbs:
            if n.pos is None:
                nodes.append(n)
        if len(nodes) == 0:
            return v.pos[0], v.pos[0]

        angle = (max_angle - min_angle) / len(nodes)

        for i,n in enumerate(nodes):
            nangle = min_angle + (i+0.5)*angle
            n.pos = (v.pos[0]+math.cos(nangle), v.pos[1]+math.sin(nangle))

        for i,n in enumerate(nodes):
            max_x_tmp, min_x_tmp = self.recurse_layout(n, min_angle+i*angle, min_angle+(i+1)*angle)
            if max_x_tmp > max_x:
                max_x = max_x_tmp
            if min_x_tmp < min_x:
                min_x = min_x_tmp
        return max_x, min_x

    def visualize(self, layout_func=generate_layout):
        layout_func(self)
        xy = np.zeros((len(self.V), 2))
        for i, v in enumerate(self.V):
            xy[i] = v.pos
        plt.scatter(xy[:,0], xy[:,1])

        for e in self.E:
            plt.plot((self.V[e[0]].pos[0], self.V[e[1]].pos[0]), (self.V[e[0]].pos[1], self.V[e[1]].pos[1]), c='black')
        plt.show()


class DirectedGraph(Graph):
    def build_neighbors(self):
        for e in self.E:
            self.V[e[0]].nbs.add(self.V[e[1]])



class ErdosRenyi(Graph):
    def __init__(self, n, lb, seed=None):
        v = [Graph.Node(None) for _ in range(n)]
        if seed is not None:
            random.seed(a=seed)
        e = set([(i,j) for i in range(n) for j in range(i,n) if random.uniform(0,1) <= lb/n])
        super(ErdosRenyi, self).__init__(v,e)

