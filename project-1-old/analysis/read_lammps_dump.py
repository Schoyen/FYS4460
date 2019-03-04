import pandas as pd
import re


HEADERS_2D = ["id", "type", "x", "y", "vx", "vy"]
HEADERS_3D = ["id", "type", "x", "y", "z", "vx", "vy", "vz"]


def read_atoms(filename, num_dimensions=3):
    float_pattern = r"[-+]?\d+\.?\d*[eE]?[-+]?\d*"
    pattern = r"^\d+[ \t]\d+"

    for i in range(2 * num_dimensions):
        pattern += r"[ \t]" + float_pattern

    with open(filename, "r") as f:
        return re.findall(pattern, f.read(), flags=re.MULTILINE)


def read_dump(filename, num_dimensions=3):
    headers = HEADERS_3D if num_dimensions == 3 else HEADERS_2D
    dat = read_atoms(filename, num_dimensions=num_dimensions)
    dat = "\n".join(dat)

    return pd.read_csv(
        pd.compat.StringIO(dat), sep=" ", index_col=False, names=headers
    )


if __name__ == "__main__":
    df = read_dump("dump.lammpstrj")
    print(len(df))
    print(df.head())
    print(df.tail())
