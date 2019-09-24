from graphs import *

# v = [Graph.Node(None) for _ in range(6)]
# e = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (3, 4), (4, 5)}
# g = Graph(v,e)
g = ErdosRenyi(10,5)
# print(g.V)
print(g.E)
g.visualize()