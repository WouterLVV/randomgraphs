import matplotlib.pyplot as plt
import math
import numpy as np
import random
import functools
import matplotlib.animation as animation
from collections import deque


class Graph:
    class Node:

        def __init__(self, _nbs, _id=-1):
            self.nbs = _nbs
            self.id = _id
            if self.nbs is None:
                self.nbs = set()

        def __str__(self):
            return str(self.id) + " -- " + ",".join([str(v.id) for v in self.nbs]) if self.id >= 0 else "Node"

    def __init__(self, _V: list, _E: set):
        self.V = _V
        self.E = _E
        self.edgelist = [e for e in self.E]
        self.line_ctr = 0
        self.build_neighbors()

    def build_neighbors(self):
        for e in self.E:
            self.V[e[0]].nbs.add(self.V[e[1]])
            self.V[e[1]].nbs.add(self.V[e[0]])

    def generate_layout(self, max_nbs=0):
        for v in self.V:
            v.pos = None
        self.V[0].pos = (0., 0.)
        max_x, min_x = self.iterate_layout(self.V[0], 0, math.tau, max_nbs=max_nbs)
        for i in range(len(self.V)):
            if self.V[i].pos == None:
                self.V[i].pos = (0, 0)
                max_x += 1
                max_x_tmp, min_x_tmp = self.iterate_layout(self.V[i], 0, math.tau, max_nbs=max_nbs)
                offset = max_x - min_x_tmp
                q = [self.V[i]]
                while len(q) > 0:
                    current = q.pop()
                    current.pos = (current.pos[0] + offset, current.pos[1])
                    for nb in current.nbs:
                        if nb.pos is not None and nb.pos[0] < max_x:
                            q.append(nb)
                max_x = max_x + max_x_tmp - min_x_tmp

    def iterate_layout(self, start, min_angle, max_angle, max_nbs=0):
        start.pos = (0., 0.)
        q = deque()
        q.append((start, min_angle, max_angle))
        max_x = 0
        min_x = 0
        while (len(q) != 0):
            v, min_angle, max_angle = q.popleft()
            nodes = []

            for n in v.nbs:
                if n.pos is None:
                    nodes.append(n)
                    if max_nbs > 0 and len(nodes) >= max_nbs:
                        break
            if len(nodes) == 0:
                if v.pos is not None:
                    if v.pos[0] > max_x:
                        max_x = v.pos[0]
                    if v.pos[0] < min_x:
                        min_x = v.pos[0]
                continue

            angle = (max_angle - min_angle) / len(nodes)

            for i, n in enumerate(nodes):
                nangle = min_angle + (i + 0.5) * angle
                n.pos = (v.pos[0] + math.cos(nangle), v.pos[1] + math.sin(nangle))
                q.append((n, min_angle + i * angle, min_angle + (i + 1) * angle))
        return max_x, min_x

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

        for i, n in enumerate(nodes):
            nangle = min_angle + (i + 0.5) * angle
            n.pos = (v.pos[0] + math.cos(nangle), v.pos[1] + math.sin(nangle))

        for i, n in enumerate(nodes):
            max_x_tmp, min_x_tmp = self.recurse_layout(n, min_angle + i * angle, min_angle + (i + 1) * angle)
            if max_x_tmp > max_x:
                max_x = max_x_tmp
            if min_x_tmp < min_x:
                min_x = min_x_tmp
        return max_x, min_x

    def draw_line(self, index):
        e = self.edgelist[index]
        plt.plot((self.V[e[0]].pos[0], self.V[e[1]].pos[0]), (self.V[e[0]].pos[1], self.V[e[1]].pos[1]), c='black')
        # self.line_ctr += 1

    def visualize(self, max_nbs=0, animated=False, animation_frametime=200):
        self.generate_layout(max_nbs=max_nbs)
        xy = np.zeros((len(self.V), 2))
        for i, v in enumerate(self.V):
            xy[i] = v.pos
        fig = plt.figure()
        plt.scatter(xy[:, 0], xy[:, 1])
        plt.gca().set_aspect('equal', adjustable='box')
        bottom, top = plt.ylim()
        if bottom > -1:
            bottom = -1.
        if top < 1:
            top = 1
        plt.ylim(bottom, top)
        self.line_ctr = 0

        if animated:
            ani = animation.FuncAnimation(fig, self.draw_line, len(self.edgelist), interval=animation_frametime,
                                          repeat=False)
        else:
            for i in range(len(self.edgelist)):
                self.draw_line(i)

        plt.show()


class DirectedGraph(Graph):
    def build_neighbors(self):
        for e in self.E:
            self.V[e[0]].nbs.add(self.V[e[1]])


class ErdosRenyi(Graph):
    def __init__(self, n, p):
        v = [Graph.Node(None, i) for i in range(n)]
        e = set([(i, j) for i in range(n) for j in range(i + 1, n) if random.uniform(0, 1) <= p])
        super(ErdosRenyi, self).__init__(v, e)


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


# Integer square root borrowed from http://code.activestate.com/recipes/577821-integer-square-root-function/
# It is faster for large numbers and has the standard infinite integer precision.
def isqrt(x):
    if x < 0:
        raise ValueError('square root not defined for negative numbers')
    n = int(x)
    if n == 0:
        return 0
    a, b = divmod(n.bit_length(), 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


"""
This function takes a number i between 0 and (n*(n-1))//2 and turns it into
a unique pair of numbers (a, b) where a < b and a,b < n
"""


def num_to_pair(i, n):
    x = 2 * n - 1
    z = x - isqrt(x * x - 8 * (i + 1))
    a = ((z + 1) // 2) - 1
    b = (n - 1) - (i - ((2 * n - a - 1) * a) // 2)
    return a, b


class MinimalistGraph:
    def __init__(self, n, _E):
        self.V = []
        self.E = _E
        for _ in range(n):
            self.V.append(set())
        for (a, b) in self.E:
            self.V[a].add(b)
            self.V[b].add(a)


class ErdosRenyiMinimalist(MinimalistGraph):
    def __init__(self, n, p):
        if p <= 0.05:
            e = self.init_small_p(n, p)
        else:
            e = self.init_large_p(n, p)
        super(ErdosRenyiMinimalist, self).__init__(n, e)

    """
    If the p is small then it is not useful to loop over every possible combination of nodes.
    Instead we use the property that the amount of edges is a binomial distribution. 
    We then calculate the amount edges that /should/ exist and then assign those edges to random node pairs in such
    a way that every possible combination of nodes occurs at most once.
    """

    def init_small_p(self, n, p):
        num_e = np.random.binomial((n * (n - 1)) // 2, p)
        if num_e == 0:
            return set()
        encoded = random.sample(range((n * (n - 1)) // 2), num_e)
        f = np.vectorize(functools.partial(num_to_pair, n=n))
        e = f(encoded)
        return set(zip(e[0], e[1]))

    def init_large_p(self, n, p):
        e = set([(i, j) for i in range(n) for j in range(i + 1, n) if random.uniform(0, 1) < p])
        return e
