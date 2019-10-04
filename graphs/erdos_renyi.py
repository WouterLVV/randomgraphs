from graphs.graph import Graph, MinimalistGraph
import functools
import numpy as np
import random

class ErdosRenyi(Graph):
    def __init__(self, n, p):
        v = [Graph.Node(None, i) for i in range(n)]
        e = set([(i, j) for i in range(n) for j in range(i + 1, n) if np.random.uniform(0, 1) <= p])
        super(ErdosRenyi, self).__init__(v, e)


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
        e = set([(i, j) for i in range(n) for j in range(i + 1, n) if np.random.uniform(0, 1) < p])
        return e
