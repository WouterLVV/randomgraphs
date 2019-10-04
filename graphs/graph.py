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

        def __str__(self):
            return str(self.id) + " -- " + ",".join([str(v.id) for v in self.nbs]) if self.id >= 0 else "Node"

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