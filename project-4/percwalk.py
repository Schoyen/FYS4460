import numba
import numpy as np


@numba.njit(cache=True)
def parallel_percwalk(spanning_cluster, num_walks, num_walkers, num_systems):
    msd = np.zeros(num_walks)

    for system in range(num_systems):
        msd += squared_displacement(spanning_cluster, num_walks, num_walkers)

    return msd / num_systems


@numba.njit(cache=True)
def squared_displacement(spanning_cluster, num_walks, num_walkers):
    displacements = np.zeros(num_walks)

    for walker in range(num_walkers):
        num_steps = 0

        while num_steps <= 1:
            _, _displacements, num_steps = percwalk(spanning_cluster, num_walks)

        displacements += np.sum(_displacements ** 2, axis=0)

    return displacements / num_walkers


@numba.njit(cache=True)
def percwalk(spanning_cluster, num_walks):
    """Function performing a random walk on the spanning cluster.

    This code is based on the program percwalk.c written by Anders
    Malthe-Sørenssen for the course FYS4460 at the University of Oslo.

    Parameters
    ----------
    spanning_cluster : np.ndarray
        Boolean array with 1's signifying a site in the spanning cluster.
    num_walks : int
        Maximum number of walker steps to perform.

    Returns
    -------
    walker_map : np.ndarray
        A coordinate map of the walk performed. The x-coordinates are stored
        in walker_map[0] and the y-coordinates in walker_map[1].
    num_steps : int
        Number of steps performed.
    """

    walker_map = np.zeros((2, num_walks))
    displacements = np.zeros_like(walker_map)
    directions = np.zeros((2, 4), dtype=np.int64)
    neighbor_arr = np.zeros(4, dtype=np.int64)

    # Note that only x-direction can move east and west, whereas y-direction moves
    # north and south.
    directions[0, 0] = 1
    directions[1, 0] = 0
    directions[0, 1] = -1
    directions[1, 1] = 0
    directions[0, 2] = 0
    directions[1, 2] = 1
    directions[0, 3] = 0
    directions[1, 3] = -1

    # Initial random position
    c_x = np.random.rand()
    c_y = np.random.rand()

    n, m = spanning_cluster.shape

    ix = int(np.floor(n * c_x))
    iy = int(np.floor(m * c_y))

    walker_map[0, 0] = ix
    walker_map[1, 0] = iy
    step = 1

    # Check if we landed outside the spanning cluster
    if not spanning_cluster[ix, iy]:
        # Return the map with starting position and number of steps
        return walker_map, displacements, step

    while step < num_walks:
        neighbor = 0

        direction = np.random.choice(directions.shape[1])
        dr = directions[:, direction]

        iix = ix + dr[0]
        iiy = iy + dr[1]

        if 0 <= iix < n and 0 <= iiy < m and spanning_cluster[iix, iiy]:
            neighbor_arr[neighbor] = direction
            neighbor += 1

            displacements[:, step] = displacements[:, step - 1] + dr
        else:
            displacements[:, step] = displacements[:, step - 1]

        if neighbor == 0:
            continue

        c = int(np.floor(np.random.rand() * neighbor))
        c = 3 if c > 3 else c
        c = 0 if c < 0 else c

        direction = neighbor_arr[c]

        ix += directions[0, direction]
        iy += directions[1, direction]

        walker_map[0, step] = ix
        walker_map[1, step] = iy

        step += 1

    return walker_map, displacements, step + 1
