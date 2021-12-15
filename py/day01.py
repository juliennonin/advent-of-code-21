# %%
import numpy as np

# %%
def nb_increases(depths, shift=1):
    return sum(depths[shift:] > depths[:-shift])

# %%
if __name__ == "__main__":
    depths = np.loadtxt(f"../data/day01.txt", dtype=int)

    print("Part 1 —", nb_increases(depths))
    print("Part 2 —", nb_increases(depths, shift=3))
