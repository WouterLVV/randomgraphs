import time
from collections import deque

from graphs.graph import MultiGraph
import numpy as np


class PA_Graph(MultiGraph):

    def __init__(self, _m=1, _d=0., _t=1):
        self.m = _m
        self.d = _d
        self.t = _t
        self.distribution = []
        # self.starttime = time.time_ns()
        # self.timeout = 60*10**9
        super(PA_Graph, self).__init__([], dict())
        if (self.m == 1):
            for _ in range(_t):
                self.evolve()
                # if time.time_ns() > self.starttime + self.timeout:
                #     break
            self.edgelist = [(i, j, k) for ((i,j), k) in self.E.items()]
        else:
            for _ in range(self.m * _t):
                self.evolve()
            new_V, new_E = self.collapse()
            super(PA_Graph, self).__init__(new_V, new_E)

    def evolve(self):
        t = len(self.V)
        new_node_id = len(self.V)
        new_node = MultiGraph.MultiNode(dict(), new_node_id)
        self.V.append(new_node)
        self.distribution.append(new_node_id)
        p = [2 * t + 1, 2 * self.d]
        if np.random.uniform(0, sum(p)) <= p[0]:
            r = self.distribution[np.random.randint(0, len(self.distribution))]
        else:
            r = np.random.randint(0, len(self.V))
        self.E[(r, new_node_id)] = 1
        new_node.add_nb(self.V[r])
        self.V[r].add_nb(new_node)
        self.distribution.append(r)

    def collapse(self):
        new_V = []
        new_E = dict()
        t = len(self.V) // self.m
        for i in range(0, self.m * t, self.m):
            new_node = MultiGraph.MultiNode(None, len(new_V))
            new_V.append(new_node)
        for ((a, b), n) in self.E.items():
            a2 = a // self.m
            b2 = b // self.m
            new_E[(a2, b2)] = new_E.get((a2, b2), 0) + n

        return new_V, new_E

    def avg_dist2(self):
        full_dist = 0
        for v in self.V:
            v.removed = False


        for v in self.V:
            q = deque()
            seen = set()
            total_dist = 0
            q.append((v, 0))
            while len(q) > 0:
                (cur, dist) = q.popleft()
                if cur in seen or cur.removed:
                    continue
                seen.add(cur)
                cur.dist = dist
                total_dist += dist
                for nb in cur.nbs:
                    if nb not in seen and not nb.removed:
                        q.append((nb, dist+1))
            full_dist += total_dist
        return full_dist/(len(self.V)*(len(self.V)-1))

    def avg_dist(self):
        for v in self.V:
            v.removed = False
        return 2*self.full_dist_recurse(self.V[0])/(len(self.V)*(len(self.V)-1))

    def full_dist_recurse(self, start):
        # find node with highest degree and count nodes in this segment
        max_node = start
        total_amount = 0
        seen = set()
        q = deque()
        q.append(start)
        while len(q) > 0:
            cur = q.popleft()
            if cur in seen or cur.removed:
                continue
            seen.add(cur)
            total_amount += 1
            if cur.get_degree() > max_node.get_degree():
                max_node = cur

            for nb in cur.nbs:
                if nb not in seen and not nb.removed:
                    q.append(nb)

        max_node.removed = True
        if total_amount <= 1:
            return 0

        seen = set()
        total_dist = 0
        q.append((max_node, 0))
        while len(q) > 0:
            (cur, dist) = q.popleft()
            if cur in seen:
                continue
            seen.add(cur)
            cur.dist = dist
            total_dist += dist
            for nb in cur.nbs:
                if nb not in seen and not nb.removed:
                    q.append((nb, dist+1))

        node_avg_dist = dict()
        for v in max_node.nbs:
            if v != max_node:
                (vdist, cnt) = self.sum_dist(v)
                node_avg_dist[v] = (vdist, cnt)

        full_dist = 0
        for (v, (vdist, vcnt)) in node_avg_dist.items():
            full_dist += vdist*(total_amount - vcnt)

        for v in max_node.nbs:
            if v != max_node:
                full_dist += self.full_dist_recurse(v)

        return full_dist


    def sum_dist(self, start):
        q = deque()
        count = 0
        seen = set()
        total_dist = 0
        q.append(start)
        while len(q) > 0:
            cur = q.popleft()
            if cur in seen or cur.removed:
                continue
            seen.add(cur)
            count += 1
            total_dist += cur.dist
            for nb in cur.nbs:
                if nb not in seen and not nb.removed:
                    q.append(nb)
        return total_dist, count

class EdgeStepGraph(PA_Graph):
    def __init__(self, _m=1, _d=0., _t=1, _p=0.):

        # In general we want p to be a function with output between [0, 1],
        # but this allows to give floats as parameters in the init for ease of use for simple cases.
        if not callable(_p):
            tmp = _p
            _p = lambda _: tmp
        # Hack so that we don't start with an edge_step because I made bad decisions and now I will stick with them
        self.p = lambda s: 1. if len(s.V) == 0 else _p(s)



        # This version of supercalling allows you to overwrite functions that are used in init
        PA_Graph.__init__(self, _m, _d, _t)

    def edge_step(self):
        t = len(self.V)
        p = [2 * t, 2 * self.d]  # No 2t+1 because both halfedges are undetermined

        if np.random.uniform(0, sum(p)) <= p[0]:
            r1 = self.distribution[np.random.randint(0, len(self.distribution))]
        else:
            r1 = np.random.randint(0, len(self.V))

        if np.random.uniform(0, sum(p)) <= p[0]:
            r2 = self.distribution[np.random.randint(0, len(self.distribution))]
        else:
            r2 = np.random.randint(0, len(self.V))

        if r2 > r1:
            pair = (r2, r1)
        else:
            pair = (r1, r2)
        self.E[pair] = self.E.get(pair, 0) + 1
        self.distribution.append(r1)
        self.distribution.append(r2)
        self.V[r1].add_nb(self.V[r2])
        self.V[r2].add_nb(self.V[r1])

    def vertex_step(self):
        PA_Graph.evolve(self)

    def evolve(self):
        pv = self.p(self)
        if np.random.ranf() < pv:
            self.vertex_step()
        else:
            self.edge_step()


