import pandas as pd


def read_slice(dat_slice):
    dat_slice = dat_slice.split("\n")[:-1]

    timestep = int(dat_slice[1])
    num_atoms = int(dat_slice[3])
    num_dim = dat_slice[4].split().count("pp")
    bounds = []

    for i in range(num_dim):
        bound = dat_slice[5 + i].split()
        bounds.append(tuple(map(lambda x: float(x), bound)))

    headers = dat_slice[5 + num_dim].split()[2:]
    data_start = 5 + num_dim + 1

    df_slice = pd.read_csv(
        pd.compat.StringIO("\n".join(dat_slice[data_start:])),
        sep=r"\s+",
        index_col=False,
        names=headers,
    )
    df_slice["timestep"] = timestep

    return df_slice, num_atoms, bounds


def read_dump(filename):
    with open(filename, "r") as f:
        dat = f.read()

    prev_pos = 0
    current_pos = 0

    df = []

    while current_pos < len(dat):
        current_pos = dat.find("ITEM: TIMESTEP", prev_pos + 1)

        if current_pos < 0:
            current_pos = len(dat)

        dat_slice = dat[prev_pos:current_pos]
        df_slice, num_atoms, bounds = read_slice(dat_slice)

        df.append(df_slice)

        prev_pos = current_pos

    df = pd.concat(df)
    df = df.sort_values(["timestep", "id"]).reset_index()
    del df["index"]

    return df, num_atoms, bounds


if __name__ == "__main__":
    df, num_atoms, bounds = read_dump("dump.lammpstrj")
    print(num_atoms)
    print(bounds)
    print(df.head())
    print(df.tail())
