from graphs.erdos_renyi import *
from graphs.preferential_attachment import PA_Graph, EdgeStepGraph
import random
import numpy as np
from graphs.generalized import GRG
from functools import partial

# # uncomment next lines to set the random seed static instead of different on every run
# seed = 7857863  # some integer
# random.seed(a=seed)
# np.random.seed(seed=seed)

# # Basic Graph
# v = [Graph.Node(None) for _ in range(6)]
# e = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (3, 4), (4, 5)}
# g = Graph(v,e)

# # ErdosRenyi Graph with n = 10, p = 0.5
# g = ErdosRenyi(50,0.08)
# print(g.E)
# g.generate_layout()
# print([(i, v.pos) for i,v in enumerate(g.V)])
# g.visualize(max_nbs=10, animated=True, animation_frametime=1)
#
# # # A simple branching process with a binomial distribution
# func = BranchingProcess.generate_binomial_function(2,0.75)
# g = BranchingProcess(10, distribution=func)
# g.visualize()
for t in [10,20,50,100, 200, 500, 1000, 2000, 5000]: #, 10000]:
    print(t)
    g = PA_Graph(_m=1, _d=0, _t=t)
    # g.visualize(animated=False, animation_frametime=10, max_steps=1)
    print(len(g.E))
    # print(g.avg_dist2())
    print(g.avg_dist())
    print()
    # print(g.E)
    # print(len(g.edgelist))


# g = GRG.from_distribution(partial(np.random.pareto, a=2.5), 100)
# print([(v.id, v.w, v.degree()) for v in g.V])
# print(g.E)
# print(len(g.E))

# g.visualize(animated=True, animation_frametime=10, max_steps=1000)