import numpy as np


def log_bin(data, num_bins=20, base=10):
    log_max = np.ceil(np.max(np.log(data) / np.log(base)))

    bins = np.logspace(0, log_max, num_bins, base=base)
    widths = bins[1:] - bins[:-1]

    hist = np.histogram(data, bins=bins)
    hist_norm = hist[0] / widths

    return hist_norm, bins, widths
