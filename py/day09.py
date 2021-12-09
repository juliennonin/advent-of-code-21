# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
with open("../data/day09.txt", "r") as f:
    data = np.array([list(map(int, list(l))) for l in f.read().splitlines()])

data_pad = np.pad(data, 1, 'maximum')
# %%
down = data < data_pad[2:, 1:-1]
up = data < data_pad[:-2, 1:-1]
left = data < data_pad[1:-1, 2:]
right = data < data_pad[1:-1, :-2]
mask = down & up & left & right
print(((data + 1) * mask).sum())
# %%
bassins = np.where(data == 9, -1, 0) # np.zeros_like(data)
bassins = np.pad(bassins, 1, constant_values=-1)


def rec(i, j, bassins, val):
    if bassins[i, j] != 0 or data_pad[i, j] == 9:
        return 0
    bassins[i, j] = val
    return 1 + rec(i-1, j, bassins, val) + rec(i+1, j, bassins, val) \
        + rec(i, j-1, bassins, val) + rec(i, j+1, bassins, val)

T = []
for k, (i, j) in enumerate(np.argwhere(mask), 1):
    T.append(rec(i+1, j+1, bassins, k))

bassins = bassins[1:-1, 1:-1]

plt.figure(figsize=(16, 8))
plt.subplot(1,2,1)
plt.imshow(data, cmap="gist_earth_r")
plt.axis('off')
plt.subplot(1,2,2)
plt.imshow(bassins, cmap="inferno")
plt.axis('off')
plt.tight_layout()
plt.savefig("test.svg")
plt.show()

print(np.prod(sorted(T)[-3:]))
