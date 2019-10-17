import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.animation as animation
from collections import deque


class Graph:
    class Node:

        def __init__(self, _nbs, _id=-1):
            self.nbs = _nbs
            self.id = _id
            if self.nbs is None:
                self.nbs = set()

        def degree(self):
            return len(self.nbs)

        def __str__(self):
            return str(self.id) + "(" + str(self.degree()) + ")" + " -- " + ",".join([str(v.id) for v in self.nbs]) if self.id >= 0 else "Node"

    # ------------Initialization------------ #

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

    # --------------Properties-------------- #

    def components(self):
        comps = []
        visited = [False] * len(self.V)
        q = deque()
        for i in range(len(self.V)):
            if visited[i]:
                continue
            res = 1
            visited[i] = True
            q.extend(self.V[i].nbs)
            while len(q) > 0:
                cur = q.popleft()
                if visited[cur.id]:
                    continue
                visited[cur.id] = True
                res += 1
                for j in cur.nbs:
                    if not visited[j.id]:
                        q.append(j)
            comps.append(res)
        return comps

    def largestcomponent(self):
        largestcomp = 0
        visited = [False] * len(self.V)
        q = deque()
        for i in range(len(self.V)):
            if visited[i]:
                continue
            res = 1
            visited[i] = True
            q.extend(self.V[i].nbs)
            while len(q) > 0:
                cur = q.popleft()
                if visited[cur.id]:
                    continue
                visited[cur.id] = True
                res += 1
                for j in cur.nbs:
                    if not visited[j.id]:
                        q.append(j)
            if res > largestcomp:
                largestcomp = res
        return largestcomp

    def count_triangles(self):
        triangles = 0
        for (a, b) in self.E:
            triangles += len(self.V[a].nbs.intersection(self.V[b].nbs))
        return triangles // 3

    # -------------Visualization------------- #

    def force_field(self, sim_step=0.001, max_diff=0.01, node_repel=0.1, edge_attract=0.01, max_steps=1000):
        self.force_field_init(sim_step, max_diff, node_repel, edge_attract)
        steps = 0
        while steps < max_steps and not self.force_field_step():
            steps += 1

    def force_field_init(self, sim_step=0.1, max_diff=0.01, node_repel=1., edge_attract=0.5):
        self.ff_sim_step = sim_step
        self.ff_max_delta = max_diff
        self.ff_node_repel = node_repel
        self.ff_edge_attract = edge_attract
        for v in self.V:
            v.pos = np.random.uniform(0.,len(self.V), (2,))

    def force_field_step(self):
        max_delta = -1
        for v in self.V:
            delta = np.array([0., 0.])
            for w in self.V:
                if v == w:
                    continue
                diff = v.pos-w.pos
                delta += (self.ff_node_repel*diff/np.linalg.norm(diff))/len(self.V)
            for w in v.nbs:
                diff = w.pos-v.pos
                delta += (self.ff_edge_attract * diff * np.log(np.linalg.norm(diff)))/len(self.E)
            delta *= self.ff_sim_step
            v.delta = delta
            if np.linalg.norm(delta) > max_delta:
                max_delta = np.linalg.norm(delta)
        for v in self.V:
            v.pos += v.delta
        return max_delta < self.ff_max_delta

    def generate_layout(self, max_nbs=0):
        for v in self.V:
            v.pos = None
        self.V[0].pos = (0., 0.)
        max_x, min_x = self.iterate_layout(self.V[0], 0, math.tau, max_nbs=max_nbs)
        for i in range(len(self.V)):
            if self.V[i].pos is None:
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

    @staticmethod
    def iterate_layout(start, min_angle, max_angle, max_nbs=0):
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

    def draw_line(self, index):
        e = self.edgelist[index]
        plt.plot((self.V[e[0]].pos[0], self.V[e[1]].pos[0]), (self.V[e[0]].pos[1], self.V[e[1]].pos[1]), c='black')


    def viz_step(self, index):
        plt.clf()
        self.force_field_step()
        xy = np.zeros((len(self.V), 2))
        for i, v in enumerate(self.V):
            xy[i] = v.pos
        plt.scatter(xy[:, 0], xy[:, 1])
        for i in range(len(self.edgelist)):
            self.draw_line(i)
        plt.gca().set_aspect('equal', adjustable='box')
        bottom, top = plt.ylim()
        if bottom > -1:
            bottom = -1.
        if top < 1:
            top = 1
        plt.ylim(bottom, top)

    def visualize(self, max_nbs=0, animated=False, animation_frametime=200, max_steps=10):
        # self.generate_layout(max_nbs=max_nbs)
        self.force_field_init(edge_attract=0.01, sim_step=10., node_repel=2.)
        fig = plt.figure()

        if animated:
            ani = animation.FuncAnimation(fig, self.viz_step, max_steps, interval=animation_frametime,
                                          repeat=False)
        else:
            for i in range(len(self.edgelist)):
                self.draw_line(i)

        plt.show()


class DirectedGraph(Graph):
    def build_neighbors(self):
        for e in self.E:
            self.V[e[0]].nbs.add(self.V[e[1]])


class MinimalistGraph:
    def __init__(self, n, _E):
        self.V = []
        self.E = _E
        for _ in range(n):
            self.V.append(set())
        for (a, b) in self.E:
            self.V[a].add(b)
            self.V[b].add(a)

    def components(self):
        comps = []
        visited = [False] * len(self.V)
        q = deque()
        for i in range(len(self.V)):
            if visited[i]:
                continue
            res = 1
            visited[i] = True
            q.extend(self.V[i])
            while len(q) > 0:
                cur = q.popleft()
                if visited[cur]:
                    continue
                visited[cur] = True
                res += 1
                for j in self.V[cur]:
                    if not visited[j]:
                        q.append(j)
            comps.append(res)
        return comps

    def largestcomponent(self):
        largestcomp = 0
        visited = [False] * len(self.V)
        q = deque()
        for i in range(len(self.V)):
            if visited[i]:
                continue
            res = 1
            visited[i] = True
            q.extend(self.V[i])
            while len(q) > 0:
                cur = q.popleft()
                if visited[cur]:
                    continue
                visited[cur] = True
                res += 1
                for j in self.V[cur]:
                    if not visited[j]:
                        q.append(j)
            if res > largestcomp:
                largestcomp = res
        return largestcomp

    # destructive is faster (usually)
    def count_triangles_minimalist(self, destructive=False):
        triangles = 0
        if not destructive:
            for (a, b) in self.E:
                triangles += len(self.V[a].intersection(self.V[b]))
            triangles //= 3
        else:
            for (a, b) in self.E:
                s = self.V[a].intersection(self.V[b])
                triangles += len(s)
                self.V[a].remove(b)
                self.V[b].remove(a)
        return triangles