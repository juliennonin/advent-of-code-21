# %%
import bisect
import numpy as np

# %%
def find_lowest_coords(mmap):
    mmap_pad = np.pad(mmap, 1, constant_values=9) # or "maximum"
    down = mmap < mmap_pad[2:, 1:-1]
    up = mmap < mmap_pad[:-2, 1:-1]
    left = mmap < mmap_pad[1:-1, 2:]
    right = mmap < mmap_pad[1:-1, :-2]
    return down & up & left & right

def bassin_size_around_loc(i, j, bassins, color=1):
    if bassins[i, j] != 0:  # boundary (border or 9) or already visited
        return 0
    bassins[i, j] = color
    nb_neighbours = bassin_size_around_loc(i-1, j, bassins, color) \
        + bassin_size_around_loc(i+1, j, bassins, color) \
        + bassin_size_around_loc(i, j-1, bassins, color) \
        + bassin_size_around_loc(i, j+1, bassins, color)
    return 1 + nb_neighbours

def find_biggest_bassins(mmap, seeds, N=3):
    bassins = np.where(mmap == 9, -1, 0)  # mark all 9 as boundaries
    bassins = np.pad(bassins, 1, constant_values=-1)  # for safety
    biggest = [0] * N
    for k, (i, j) in enumerate(seeds, start=1):
        size = bassin_size_around_loc(i + 1, j + 1, bassins, k)  # +1 because of padding
        if size > biggest[0]:
            bisect.insort(biggest, size)
            biggest.pop(0)
    return biggest

# %%
if __name__ == "__main__":
    with open("../data/day09.txt", "r") as f:
        data = np.array([list(map(int, list(l))) for l in f.read().splitlines()])

    mask = find_lowest_coords(data)
    part1 = np.sum((data + 1) * mask)
    part2 = np.prod(find_biggest_bassins(data, np.argwhere(mask)))

    print("Part 1 —", part1)
    print("Part 2 —", part2)

