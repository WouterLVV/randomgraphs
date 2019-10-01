from graphs import *
import time
import functools

def count_triangles(g):
    triangles = 0
    for (a,b) in g.E:
        triangles += len(g.V[a].nbs.intersection(g.V[b].nbs))
    return triangles//3


class MinimalistGraph:

    def __init__(self, n, _E):
        self.V = []
        self.E = _E
        for _ in range(n):
            self.V.append(set())
        for (a,b) in self.E:
            self.V[a].add(b)
            self.V[b].add(a)

class ErdosRenyiMinimalist(MinimalistGraph):
    def __init__(self, n, p):
        if p <= 0.05:
            e = self.init_small_p(n, p)
        else:
            e = self.init_large_p(n, p)
        super(ErdosRenyiMinimalist, self).__init__(n, e)

    def init_small_p(self, n, p):
        num_e = np.random.binomial((n*(n-1))//2, p)
        encoded = random.sample(range((n*(n-1))//2), num_e)
        f = np.vectorize(functools.partial(num_to_pair, n=n))
        e = f(encoded)
        return set(zip(e[0],e[1]))

    def init_large_p(self, n, p):
        e = set([(i, j) for i in range(n) for j in range(i+1, n) if random.uniform(0, 1) < p])
        return e


def num_to_pair(i, n):
    x = 2 * n - 1
    z = x - isqrt(x * x - 8 * (i + 1))
    a = ((z+1) // 2) -1
    b = (n-1)-(i-((2*n-a-1)*a)//2)
    return a, b

# Integer square root
def isqrt(x):
    if x < 0:
        raise ValueError('square root not defined for negative numbers')
    n = int(x)
    if n == 0:
        return 0
    a, b = divmod(n.bit_length(), 2)
    x = 2**(a+b)
    while True:
        y = (x + n//x)//2
        if y >= x:
            return x
        x = y

# destructive is faster
def count_triangles_minimalist(g, destructive=False):
    triangles = 0
    if not destructive:
        for (a,b) in g.E:
            triangles += len(g.V[a].intersection(g.V[b]))
        triangles //= 3
    else:
        for (a,b) in g.E:
            s = g.V[a].intersection(g.V[b])
            triangles += len(s)
            g.V[a].remove(b)
            g.V[b].remove(a)
    return triangles


# seed = 1  # some integer
# random.seed(a=seed)
# np.random.seed(seed=seed)


# n = 1000
# for i in range((n*(n-1))//2):
#     print(num_to_pair(i, n))


# lb = 100
# ln = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]
# repetitions = 10
# ys1 = []
# ys2 = []
# for n in ln:
#     sum1 = 0
#     sum2 = 0
#     for _ in range(repetitions):
#         g = ErdosRenyiMinimalist(n, lb/n)
#         sum1 += count_triangles_minimalist(g, destructive=True)
#         sum2 += np.random.poisson((lb**3)/6)
#     ys1.append(sum1/repetitions)
#     ys2.append(sum2/repetitions)
#
# print(ys1)
# print(ys2)
# plt.figure()
# plt.scatter(ln, ys1, c='b')
# plt.scatter(ln, ys2, c='r')
# plt.show()

# print(g.E)
# g.visualize()