from graphs.erdos_renyi import *
from multiprocessing import Pool
import matplotlib.pyplot as plt


def count_triangles(g):
    triangles = 0
    for (a, b) in g.E:
        triangles += len(g.V[a].nbs.intersection(g.V[b].nbs))
    return triangles // 3


# destructive is faster (usually)
def count_triangles_minimalist(g, destructive=False):
    triangles = 0
    if not destructive:
        for (a, b) in g.E:
            triangles += len(g.V[a].intersection(g.V[b]))
        triangles //= 3
    else:
        for (a, b) in g.E:
            s = g.V[a].intersection(g.V[b])
            triangles += len(s)
            g.V[a].remove(b)
            g.V[b].remove(a)
    return triangles


#destructive
def count_triangles_minimalist_nodewise(g):
    triangles = 0
    for vi in range(len(g.V)):
        nbl = sorted([nb for nb in g.V[vi]])
        for i in range(len(nbl)):
            g.V[nbl[i]].remove(vi)
            for j in range(i+1, len(nbl)):
                if (nbl[i], nbl[j]) in g.E:
                    triangles += 1
    return triangles

seed = 12341345  # some integer
random.seed(a=seed)
np.random.seed(seed=seed)



repetitions = 100
lb = 60
n = 600000
g = ErdosRenyiMinimalist(n, lb/n)

print(count_triangles_minimalist(g, destructive=False))
exit()
# print(count_triangles_minimalist_nodewise(g))
# exit()
# n = 1000
# for i in range((n*(n-1))//2):
#     print(num_to_pair(i, n))



def trial(n):
    res = []
    for _ in range(repetitions):
        g = ErdosRenyiMinimalist(n, lb / n)
        res.append(count_triangles_minimalist(g, destructive=True))
    return res
    # ys2.append(sum2/repetitions)


if __name__ == '__main__':
    max_n = 200
    ns = []
    ns.extend(range(lb, 100, 1))
    ns.extend(range(100, 200, 2))
    ns.extend(range(200, 400, 4))
    ns.extend(range(400, 800, 8))
    ns.extend(range(800, 1600, 16))
    ns.extend(range(1600, 3200, 32))
    ns.extend(range(3200, 6400, 64))
    ns.extend(range(6400, 12800, 128))
    ns.extend(range(12800, 25600, 256))

    threads = 10

    p = Pool(processes=threads)

    ys1 = ns.copy()
    pois = np.random.poisson((lb ** 3) / 6, repetitions)

    ys1 = p.map(trial, ys1, chunksize=10)

    coeff = (lb ** 3) / 6
    avgs = [i for i in map(np.average, ys1)]
    vars = [i for i in map(np.var, ys1)]

    print(coeff)
    print(avgs)
    print(vars)

    plt.figure()
    plt.scatter(ns, avgs, c='b')
    plt.scatter(ns, vars, c='r')
    plt.plot((lb, max(ns)), (coeff, coeff), c='g')
    plt.show()
