from graphs import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def components(g):
    comps = []
    visited = [False] * len(g.V)
    q = deque()
    for i in range(len(g.V)):
        if visited[i]:
            continue
        res = 1
        visited[i] = True
        q.extend(g.V[i])
        while len(q) > 0:
            cur = q.popleft()
            if visited[cur]:
                continue
            visited[cur] = True
            res += 1
            for j in g.V[cur]:
                if not visited[j]:
                    q.append(j)
        comps.append(res)
    return comps


def largestcomponent(g):
    largestcomp = 0
    visited = [False] * len(g.V)
    q = deque()
    for i in range(len(g.V)):
        if visited[i]:
            continue
        res = 1
        visited[i] = True
        q.extend(g.V[i])
        while len(q) > 0:
            cur = q.popleft()
            if visited[cur]:
                continue
            visited[cur] = True
            res += 1
            for j in g.V[cur]:
                if not visited[j]:
                    q.append(j)
        if res > largestcomp:
            largestcomp = res
    return largestcomp


lbs = np.arange(0.1, 3., 0.1)
ns = []
ns.extend(range(1, 100, 1))

repetitions = 100
res = []
for lb in lbs:
    for n in ns:
        comps = sum([largestcomponent(ErdosRenyiMinimalist(n, lb / n)) / n for _ in range(repetitions)]) / repetitions
        res.append((lb, n, comps))
res = np.array(res)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(res[:, 0], res[:, 1], res[:, 2], c=cm.hot(np.abs(res[:, 2] / 1.1)))
ax.set_xlabel('lambda')
ax.set_ylabel('n')
ax.set_zlabel('fraction of largest component')
plt.show()