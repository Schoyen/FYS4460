import numba
import numpy as np
import scipy.ndimage
import skimage


@numba.njit(cache=True)
def hypot(a, b):
    return np.sqrt(a ** 2 + b ** 2)


@numba.njit(cache=True)
def taxi_distance(a, b):
    return int(np.ceil(hypot(a, b)))


@numba.njit(cache=True)
def _correlation_function(labels, g, norm):
    L = len(labels)

    for ix_1 in range(L):
        for iy_1 in range(L):
            site_1 = labels[ix_1, iy_1]

            for ix_2 in range(L):
                for iy_2 in range(L):
                    site_2 = labels[ix_2, ix_2]
                    dx = ix_2 - ix_1
                    dy = iy_2 - iy_1

                    g_ind = taxi_distance(dx, dy)

                    g[g_ind] += (site_1 == site_2) * (site_1 > 0)
                    norm[g_ind] += 1


def correlation_function(p, L):
    system = np.random.rand(L, L)
    mat = system < p

    labels, num_features = scipy.ndimage.measurements.label(mat)

    # Correlation function
    g = np.zeros(2 * L)
    norm = np.zeros_like(g)

    _correlation_function(labels, g, norm)

    return g[g > 0] / norm[g > 0]
