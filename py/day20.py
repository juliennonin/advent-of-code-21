# %%
import numpy as np
from scipy import signal

# %%
BINARY_FILTER = 2 ** np.arange(9).reshape(3, 3)

def get_enhancer_mappings(mappings):
    return  np.vectorize(lambda n: mappings[n])

def image_processing(img, enhancer, n):
    out = np.copy(img)
    fill_value = 0
    for _ in range(n):
        out = np.pad(out, 2, constant_values=fill_value)
        out = signal.convolve2d(out, BINARY_FILTER, mode="valid").astype(int)
        out = enhancer(out)
        fill_value = enhancer(fill_value)
    return out
# %%
if __name__ == "__main__":
    with open("../data/day20.txt", "r") as f:
        mappings, img = f.read().replace('.', '0').replace('#', '1').split("\n\n")
        mappings = [int(b) for b in mappings]
        img = np.array([list(map(int, line)) for line in img.splitlines()])
        assert len(mappings) == 512

    enhancer = get_enhancer_mappings(mappings)

    part1 = image_processing(img, enhancer, 2).sum()
    part2 = image_processing(img, enhancer, 50).sum()

    print("Part 1 —", part1)
    print("Part 2 —", part2)
