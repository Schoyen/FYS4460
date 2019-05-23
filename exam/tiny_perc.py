import itertools

import tqdm
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt


def compute_probability_of_configuration(c_i, p, L):
    k = int(np.sum(c_i))

    return p ** k * (1 - p) ** (L ** 2 - k)


def is_spanning(system):
    L = system.shape[0]

    if L == 1:
        return system[0, 0]

    label, num_features = scipy.ndimage.measurements.label(system)

    x_direction = np.any(np.intersect1d(label[:, 0], label[:, 1]) > 0)
    y_direction = np.any(np.intersect1d(label[0], label[1]) > 0)

    return x_direction or y_direction


def compute_condition_scd(c_i, g_i, p, L):
    if np.sum(c_i) < L:
        return 0

    scd = np.sum(c_i) / L ** 2
    prob = compute_probability_of_configuration(c_i, p, L)

    num_spanning = 0

    for configuration in g_i:
        if is_spanning(configuration):
            num_spanning += 1

    return num_spanning * scd * prob


def compute_spanning_cluster_density(c, g, p, L):
    scd = 0

    for key in c:
        scd += compute_condition_scd(c[key], g[key], p, L)

    return scd


def compute_condition_pp(c_i, g_i, p, L):
    if np.sum(c_i) < L:
        return 0


def compute_percolation_probability(c, g, p, L):
    pass


def sort_configurations(c, g):
    non_spanning_c = {}
    non_spanning_g = {}
    spanning_c = {}
    spanning_g = {}

    counter = 1

    for key in c:
        non_spanning_c[counter] = []
        non_spanning_g[counter] = []
        spanning_c[counter] = []
        spanning_g[counter] = []
        any_spanning = False
        any_non_spanning = False

        for configuration in g[key]:
            if is_spanning(configuration):
                pass

        if any_spanning:
            spanning_c[counter].append(c[key])
        if any_non_spanning:
            non_spanning_c[counter].append(c[key])

        counter += 1


def create_configurations(L):
    c = {}
    g = {}

    for i in range(L ** 2 + 1):
        c[i + 1] = [1] * i + [0] * (L ** 2 - i)
        g[i + 1] = []

        for perm in set(itertools.permutations(c[i + 1])):
            comb = []
            for j in range(L):
                comb.append(perm[j * L : (j + 1) * L])

            g[i + 1].append(np.array(comb))

    return sort_configurations(c, g)


L_list = [1, 2, 3]

p_arr = np.linspace(0, 1, 101)
scd_arr = np.zeros((len(L_list), len(p_arr)))

for i, L in enumerate(L_list):
    c, g = create_configurations(L)

    for j, p in tqdm.tqdm(enumerate(p_arr), total=len(p_arr)):
        scd_arr[i, j] = compute_spanning_cluster_density(c, g, p, L)

    plt.plot(p_arr, scd_arr[i], label=fr"$L = {L}$")

plt.legend(loc="best")
plt.show()
