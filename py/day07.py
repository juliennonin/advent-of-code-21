# %%
import numpy as np

# %%
if __name__ == "__main__":
    h = np.loadtxt("../data/day07.txt", delimiter=',', dtype=int)
    # h = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])  # uncomment for testing
    
    part1 = np.abs(h - int(np.median(h))).sum()  # analytical solution
    # part1 = np.min([np.abs(h - i).sum() for i in range(max(h) + 1)])

    # part2 
    part2 = np.min([((h - i) ** 2 + np.abs(h - i)).sum() for i in range(max(h) + 1)]) // 2

    print("Part 1 —", part1)
    print("Part 2 —", part2)


