import numba
import numpy as np
import math


@numba.njit(cache=True)
def generate_correlation_power_law(l, alpha):
    L = int(2 ** l)
    N = L * L

    C = np.zeros(N)

    for index in range(N):
        r_2 = 0
        _index = index

        for dim in range(2):
            r_i = _index % L

            r_i = r_i if r_i < (L / 2) + 1 else r_i - L
            r_2 += r_i * r_i
            _index /= L

        C[index] = (1 + r_2) ** (-0.5 * alpha)

    return C


@numba.njit(cache=True)
def fill_g(phi, u, N):
    g = np.zeros(N, dtype=np.complex128)

    for j in range(N):
        val = 0

        for k in range(N):
            val += phi[j - k] * u[k]

        g[j] += val

    return g


def generate_correlated_system(l, alpha=0.5):
    """An implementation of the algorithm decribed in:
    https://doi.org/10.1016/0960-0779(95)80035-F

    This implementation is a Python version of the C++-code found here:
    https://github.com/CQT-Leipzig/correlated_disorder
    """
    L = int(2 ** l)
    N = L * L

    u = np.random.normal(0, 1, size=N)
    U = np.fft.fft(u)

    C = generate_correlation_power_law(l, alpha=alpha)
    S_k = np.fft.fft(C)
    S_k[S_k < 0] = 0

    response = np.sqrt(S_k) * np.abs(U)

    phi = np.fft.ifft(response)

    return fill_g(phi, u, N).reshape(L, L)


@numba.njit(cache=True)
def calculate_p_from_theta(theta, sigma=1.0):
    return 0.5 * math.erfc((-theta) / math.sqrt(2 * sigma))


@numba.njit(cache=True)
def calculate_theta(p, sigma=1.0, tol=1e-8):
    p_i = 0
    theta = 0

    theta_min = -5 * np.sqrt(sigma)
    theta_max = 5 * np.sqrt(sigma)

    while abs(p - p_i) > tol:
        p_i = calculate_p_from_theta(theta, sigma)

        if p_i < p:
            theta_min = theta
        else:
            theta_max = theta

        theta = theta_min + (theta_max - theta_min) / 2

    return theta


if __name__ == "__main__":
    import scipy.ndimage
    import matplotlib.pyplot as plt

    g = generate_correlated_system(8, alpha=0.5)

    p = 0.48
    theta = calculate_theta(p)

    plt.matshow((g.real < theta).astype(int))
    plt.colorbar()
    plt.show()

    labels, num_features = scipy.ndimage.measurements.label(
        (g.real < theta).astype(int)
    )
    plt.matshow(labels)
    plt.colorbar()
    plt.show()
