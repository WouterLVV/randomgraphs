import numpy as np
from graphs.generalized import GRG_degrees
from functools import partial
import matplotlib.pyplot as plt
from matplotlib import cm
from collections import Counter
from multiprocessing import pool


def hacky_latex():
    ns = [10, 20, 50, 100, 200, 400, 1000, 2000, 4000]
    m = 100
    for n in ns:
        print("\\begin{figure}[H]\n    \\begin{subfigure}[b]{0.5\\textwidth}\n        \\centering\n        \\includegraphics[width=\\textwidth]{fig/hw3/grg_raw_n" + str(n) + "_m" + str(m) + ".pdf}\n        \\caption{Every degree plotted for n = " + str(n) + "}\n    \\end{subfigure}\n    \\begin{subfigure}[b]{0.5\\textwidth}\n        \\centering\n        \\includegraphics[width=\\textwidth]{fig/hw3/grg_dist_n" + str(n) + "_m" + str(m) + ".pdf}\n        \\caption{Average and variance plotted for n = " + str(n) + "}\n    \\end{subfigure}\n\\end{figure}")
        # "fig/hw3/grg_raw_n" + str(n) + "_m" + str(m) + ".pdf"
        # "fig/hw3/grg_raw_n" + str(n) + "_m" + str(m) + ".pdf"

def worker(i, w):
    return GRG_degrees(w)


if __name__ == '__main__':
    # uncomment next lines to set the random seed static instead of different on every run
    # seed = 7857863  # some integer
    # random.seed(a=seed)
    # np.random.seed(seed=seed)

    ns = [10, 20, 50, 100, 200, 400, 1000, 2000, 4000]
    m = 100

    for n in ns:

        w = np.random.pareto(a=1.5, size=n)
        w.sort()

        func = partial(worker, w=w)
        p = pool.Pool(processes=10)
        degrees = np.array(p.map(func, range(m)))

        avg = np.zeros((n,), dtype=np.float)
        var = np.zeros((n,), dtype=np.float)
        for i in range(n):
            dis = degrees[:,i]
            avg[i] = np.average(dis)
            var[i] = np.var(dis)

        plt.figure()
        for i in range(n):
            dis = degrees[:,i]
            c = Counter(dis)
            maxval = max(c.values())
            counts = np.array([(k,v) for (k, v) in c.items()])
            plt.scatter([i for _ in range(len(counts))], counts[:, 0], s=(100./n), marker='.', c=cm.hot(1-(counts[:,1]/maxval)))
        plt.scatter(range(n), w, s=(100./n), c='g', marker='.', label="weights")
        plt.legend()
        plt.savefig("outputs/grg_raw_n" + str(n) + "_m" + str(m) + ".pdf", dpi=300)

        plt.figure()
        plt.scatter(range(n), avg, s=(100./n), marker='o', c='b', label="average")
        plt.scatter(range(n), var, s=(100./n), marker='o', c='r', label="variance")
        plt.scatter(range(n), w,   s=(100./n), marker='o', c='g', label="weights")
        plt.legend()
        plt.savefig("outputs/grg_dist_n" + str(n) + "_m" + str(m) + ".pdf", dpi=300)

        # plt.show()
