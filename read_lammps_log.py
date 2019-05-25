import os
import re

import pandas as pd


def get_temp_lognames(prefix, extension=".log", dat_dir="dat"):
    file_list = list(
        filter(lambda x: x.startswith(prefix), os.listdir(dat_dir))
    )

    pattern = prefix + r"_(.+).log"
    temperature_list = [
        float(re.search(pattern, filename).group(1)) for filename in file_list
    ]

    file_list = list(map(lambda x: os.path.join(dat_dir, x), file_list))

    return zip(*sorted(zip(temperature_list, file_list)))


def read_log(filename):
    skiprows = 0
    skipfooter = 1

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("Step"):
                break
            skiprows += 1
        for line in f:
            if line.startswith("Loop"):
                break
        for line in f:
            skipfooter += 1

    log_df = pd.read_csv(
        filename,
        sep=r"\s+",
        skiprows=skiprows,
        skipfooter=skipfooter,
        engine="python",
    )

    return log_df


def read_rdf_log(filename):
    n = 0
    key = None
    bin_centers = {}
    g_r = {}

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue

            line = line.split()
            if len(line) == 2:
                key = int(line[0])
                n = int(line[1])

                bin_centers[key] = []
                g_r[key] = []
                continue

            bin_centers[key].append(float(line[1]))
            g_r[key].append(float(line[2]))

    return bin_centers, g_r
