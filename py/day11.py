# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
def neighbours(i, j):
    for δi in range(-1, 2):
        for δj in range(-1, 2):
            if not (δi == 0 and δj == 0):
                yield i + δi, j + δj

def chain_reaction(i, j, data):
    """" Chain reaction process starting at (i, j)
    Recursively increase the energy of octopuses adjacent to a flash
    and flash if the energy gets beyond 9
    Returns: number of flashes during the local chain reaction
    """
    if data[i, j] <= 0:  # border or has already flashed
        return 0
    # energy level increases by one due to chain reaction
    data[i, j] += 1
    if data[i, j] <= 9:
        return 0

    # if its energy level gets beyond 9:
    # 1. flashes
    data[i, j] = 0
    # 2. increase the energy level of adjacent octopuses 
    n_flashes= 1
    for ii, jj in neighbours(i, j):
        n_flashes += chain_reaction(ii, jj, data)
    return n_flashes

# %%
if __name__ == "__main__":
    with open("../data/day11.txt", "r") as f:
        data = np.array([list(map(int, list(line))) for line in f.read().splitlines()])
    
    n_octopuses = data.size
    data = np.pad(data, 1, constant_values=-1)
    N = 100
    n_flashes_after_N_step, n_flashes_step = 0, 0
    
    n = 0
    while n_flashes_step < n_octopuses:
        data[1:-1, 1:-1] += 1
        n_flashes_step = 0
        for i, j in np.argwhere(data > 9):
            n_flashes_step += chain_reaction(i, j, data)
        n += 1
        if n < N: n_flashes_after_N_step += n_flashes_step
    
    print("Part 1 —", n_flashes_after_N_step)
    print("Part 2 —", n)

