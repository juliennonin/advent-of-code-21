# %%
import numpy as np

#%%
def cost_part1(x, d):
    return np.abs(x - d).sum()

def cost_part2(x, d):
    return (((x - d) ** 2 + np.abs(x - d)) // 2).sum()

# %%
if __name__ == "__main__":
    h = np.loadtxt("../data/day07.txt", delimiter=',', dtype=int)
    # h = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])  # uncomment for testing
    
    median, mean = int(np.median(h)), int(np.mean(h))
   
    # part1 = np.min([cost_part1(h, d) for d in range(max(h) + 1)])
    # part2 = np.min([cost_part2(h, d) for d in range(max(h) + 1)])
    
    # analytical solutions
    part1 = cost_part1(h, median)
    part2 = min(cost_part2(h, mean), cost_part2(h, mean + 1))

    print("Part 1 —", part1)
    print("Part 2 —", part2)
