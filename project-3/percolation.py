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
            if prop.bbox[2] - prop.bbox[0] == L or prop.bbox[3] - prop.bbox[1] == L:
                num_percolating += 1
                break

    return num_percolating / num_samples


def compute_percolation_threshold(x, L, num_samples):
    p_bounds = (0, 1)

    def f(p):
        res = compute_percolation_probability(L, p, num_samples)

        return np.abs(res - x)

    opt = scipy.optimize.minimize_scalar(f, bounds=p_bounds, method="bounded")

    return opt.x
