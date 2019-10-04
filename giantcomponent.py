from graphs.erdos_renyi import *
from mpl_toolkits.mplot3d import Axes3D  # not useless
import matplotlib.pyplot as plt
from matplotlib import cm


lbs = np.arange(0.0, 3., 0.5)
ns = []
ns.extend(range(1, 50, 1))

repetitions = 100
res = []
for lb in lbs:
    for n in ns:
        comps = sum([ErdosRenyiMinimalist(n, lb / n).largestcomponent() / n for _ in range(repetitions)]) / repetitions
        res.append((lb, n, comps))
res = np.array(res)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(res[:, 0], res[:, 1], res[:, 2], c=cm.hot(np.abs(res[:, 2] / 1.1)))
ax.set_xlabel('lambda')
ax.set_ylabel('n')
ax.set_zlabel('fraction of largest component')
plt.show()
