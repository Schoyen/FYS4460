import warnings
import numpy as np
import scipy.ndimage
import scipy.optimize
import skimage


def compute_percolation_probability(L, p, num_samples):
    num_percolating = 0

    for i in range(num_samples):
        system = np.random.rand(L, L) < p

        labels, num_features = scipy.ndimage.measurements.label(system)
        props = skimage.measure.regionprops(labels)

        for prop in props:
            if (
                prop.bbox[2] - prop.bbox[0] == L
                or prop.bbox[3] - prop.bbox[1] == L
            ):
                num_percolating += 1
                break

    return num_percolating / num_samples


def compute_percolation_threshold(
    x,
    L,
    num_samples,
    p_bounds=(0, 1),
    tol=1e-5,
    max_iterations=100,
    verbose=False,
):
    lower, upper = p_bounds
    lower_pi, upper_pi = (0, 1)

    for i in range(max_iterations):
        if upper - lower < tol:
            break

        mid = (upper + lower) / 2
        mid_pi = compute_percolation_probability(L, mid, num_samples)

        if mid_pi > x:
            upper = mid
            upper_pi = mid_pi
        else:
            lower = mid
            lower_pi = mid_pi

    if verbose and i == max_iterations - 1:
        warnings.warn("Minimization did not converge")

    return mid
