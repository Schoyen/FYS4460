import numpy as np
import scipy.ndimage
import skimage


def get_spanning_cluster(L, p, num_attempts=1000):
    assert 0 <= p <= 1

    if not type(L) in [list, tuple, set]:
        L = (L, L)

    for attempt in range(num_attempts):
        z = np.random.rand(*L) < p

        labels, num_labels = scipy.ndimage.measurements.label(z)
        perc_labels = np.intersect1d(labels[0, :], labels[-1, :])

        perc_labels = perc_labels[perc_labels > 0]

        if len(perc_labels) > 0:
            print("Percolating cluster found")
            break

    return perc_labels, labels, num_labels, z
