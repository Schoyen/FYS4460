import math

import tqdm
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import seaborn as sns
import sympy.utilities.iterables

sns.set(color_codes=True)


def nchoosek(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def compute_probability_of_configuration(c_i, p, L):
    k = int(np.sum(c_i))

    return p ** k * (1 - p) ** (L ** 2 - k)


def is_spanning(system):
    L = system.shape[0]

    if L == 1:
        return system[0, 0]

    label, num_features = scipy.ndimage.measurements.label(system)

    x_direction = np.any(np.intersect1d(label[:, 0], label[:, -1]) > 0)
    y_direction = np.any(np.intersect1d(label[0], label[-1]) > 0)

    return x_direction or y_direction


def compute_condition_scd(c_i, g_i, p, L):
    if np.sum(c_i) < L:
        return 0

    scd = np.sum(c_i) / L ** 2
    prob = compute_probability_of_configuration(c_i, p, L)

    return len(g_i) * scd * prob


def compute_spanning_cluster_density(c, g, p, L):
    scd = 0

    for key in c:
        scd += compute_condition_scd(c[key], g[key], p, L)

    return scd


def compute_condition_pp(c_i, g_i, p, L):
    if np.sum(c_i) < L:
        return 0

    prob = compute_probability_of_configuration(c_i, p, L)

    return len(g_i) * prob


def compute_percolation_probability(c, g, p, L):
    pp = 0

    for key in c:
        pp += compute_condition_pp(c[key], g[key], p, L)

    return pp


def create_configurations(L):
    c = {}
    g_spanning = {}
    g_non_spanning = {}

    for i in range(L ** 2 + 1):
        c[i + 1] = [1] * i + [0] * (L ** 2 - i)
        g_spanning[i + 1] = []
        g_non_spanning[i + 1] = []

        total = int(nchoosek(L ** 2, i))

        for perm in tqdm.tqdm(
            sympy.utilities.iterables.multiset_permutations(c[i + 1]),
            total=total,
        ):
            comb = []
            for j in range(L):
                comb.append(perm[j * L : (j + 1) * L])

            comb = np.array(comb)

            if is_spanning(comb):
                g_spanning[i + 1].append(comb)
            else:
                g_non_spanning[i + 1].append(comb)

    return c, g_spanning, g_non_spanning


L_list = [1, 2, 3, 4, 5]

p_arr = np.linspace(0, 1, 101)
scd_arr = np.zeros((len(L_list), len(p_arr)))
pp_arr = np.zeros((len(L_list), len(p_arr)))

for i, L in enumerate(L_list):
    c, g, g_ns = create_configurations(L)

    for j, p in enumerate(p_arr):
        scd_arr[i, j] = compute_spanning_cluster_density(c, g, p, L)
        pp_arr[i, j] = compute_percolation_probability(c, g, p, L)

    plt.figure(1)
    plt.plot(p_arr, scd_arr[i], label=fr"$L = {L}$")
    plt.figure(2)
    plt.plot(p_arr, pp_arr[i], label=fr"$L = {L}$")


plt.figure(1)
plt.legend(loc="best")
plt.xlabel(r"$p$")
plt.ylabel(r"$P(p, L)$")
plt.title(r"Spanning cluster density for small systems")

plt.figure(2)
plt.legend(loc="best")
plt.xlabel(r"$p$")
plt.ylabel(r"$\Pi(p, L)$")
plt.title(r"Percolation probability for small systems")

plt.show()
