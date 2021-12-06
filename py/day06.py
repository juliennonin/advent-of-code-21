#%%
import numpy as np

# %%
def main(counts, days, period):
    """
    Args:
        counts (list): counts[k] is the number of fish whose internal clock is k
        days (int): number of days, of generations, of iterations
        period (int): number of days after which a fish spawns
    """
    assert period <= len(counts)
    for _ in range(0, days):
        counts[PERIOD] += counts[0]
        counts = np.roll(counts, -1)
    return counts


# %%
if __name__ == "__main__":
    PERIOD = 7
    PERIOD_LONG = PERIOD + 2 

    counts = np.zeros(PERIOD_LONG, dtype=int)
    with open("../data/day06.txt", "r") as f:
        for n in f.read().strip().split(','):
            counts[int(n)] += 1
    # counts = np.array([0, 1, 1, 2, 1, 0, 0, 0, 0])  # Decomment for testing

    print("Part 1 —", sum(main(counts, 80, PERIOD)))
    print("Part 2 —", sum(main(counts, 256, PERIOD)))

