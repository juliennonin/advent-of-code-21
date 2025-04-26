# %%
import numpy as np

# %%
with open('../data/day03.txt', 'r') as f:
    data = np.array([list(map(int, list(line))) for line in f.read().splitlines()], dtype=int)
# eps = (np.sign((data * 2 - 1).sum(0)) + 1) // 2
# delta = 1 - eps

# eps = int(''.join(list(map(str, eps))), 2)
# delta = int(''.join(list(map(str, delta))), 2)
# eps * delta
# %%
i = 0
while len(data) > 1 and i < data.shape[1]:
    v, c = np.unique(data[:, i], return_counts=True)
    print(v, c)
    bit = v[np.argmin(c)]
    if c[0] == c[1]:
        bit = 0
    data = data[data[:, i] == bit]
    i += 1
print(data)
print(int(''.join(list(map(str, data[0]))), 2))

# %%
# 1059 * 2808