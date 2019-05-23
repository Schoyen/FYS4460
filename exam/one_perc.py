import numpy as np
import matplotlib.pyplot as plt


p_arr = np.linspace(0.9, 0.999, 6)
L = 10000

s = np.arange(1, L + 1)

nsp = lambda s, p: (1 - p) ** 2 * p ** s

for p in p_arr:
    plt.loglog(-s * np.log(p), nsp(s, p), label=fr"$p = {p}$")

plt.legend(loc="best")
plt.show()
