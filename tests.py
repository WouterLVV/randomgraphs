from graphs import *
# # uncomment next lines to set the random seed static instead of different on every run
# seed = 7857863  # some integer
# random.seed(a=seed)
# np.random.seed(seed=seed)

# # Basic Graph
# v = [Graph.Node(None) for _ in range(6)]
# e = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (3, 4), (4, 5)}
# g = Graph(v,e)

# # ErdosRenyi Graph with n = 10, p = 0.5
# g = ErdosRenyi(10,0.5)
# print(g.E)
# g.visualize()

# A simple branching process with a binomial distribution
func = BranchingProcess.generate_binomial_function(2,0.75)
g = BranchingProcess(10, distribution=func)
g.visualize()