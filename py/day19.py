# %%
from io import StringIO
import numpy as np

# %%
def get_all_permutations():
    xp = np.array([1, 0, 0])
    yp = np.array([0, 1, 0])
    zp = np.array([0, 0, 1])
    directions = [xp, -xp, yp, -yp, zp, -zp]
    permutations = []
    for up in directions:
        for face in directions:
            # for every pair of vectors
            if np.sum(np.cross(face, up)) != 0:
                side = np.cross(up, face) # the third vector is st x ^ y = z
                permutations.append(
                    np.array([side, up, face]).T  # permutation matrix
                )
    assert len(permutations) == 24
    return permutations

PERMUTATIONS = get_all_permutations()

# %%

def find_matches(S, T):
    """"Find matches between two beacons"""
    for P in PERMUTATIONS:
        U = np.inner(P, T).T  # change orientation
        D = (S[:, np.newaxis] - U).reshape(-1, 3)  # diff btw all pairs of beacons
        points, counts = np.unique(D, return_counts=True, axis=0)
        if counts.max() == 12:
            offset = points[counts.argmax()]
            return U + offset, offset
    return None, None


def calibrate_scanners(scanners):
    N = len(scanners)
    calibrated = [0] * N  # contains the calibrated scanners
    calibrated[0] = np.copy(scanners[0])
    is_calibrated = [True] + [False] * (N - 1)
    positions = np.zeros((N, 3), dtype=int)  # positions of the scanners
    found_idx = [0]  # index of scanners already calibrated

    while not np.all(is_calibrated):
        # use an already calibrated scanner as reference
        S = calibrated[found_idx.pop()]
        for i, V in enumerate(scanners):
            # try to match with every non-calibrated scanner
            if is_calibrated[i]:
                continue
            U, pos = find_matches(S, V)
            if U is None:
                continue
            positions[i] = pos
            found_idx.append(i)
            calibrated[i] = U
            is_calibrated[i] = True
    return calibrated, positions


# %%
if __name__ == "__main__":
    with open("../data/day19.txt") as f:
        scanners = []
        for data in f.read().split("\n\n"):
            scanner = np.loadtxt(
                StringIO(data), skiprows=1, delimiter=',', dtype=int)
            scanners.append(scanner)
    
    new_scanners, positions = calibrate_scanners(scanners)
    all_offset = (positions[:, np.newaxis] - positions).reshape((-1, 3))

    part1 = len(set(map(tuple, np.vstack(new_scanners))))
    part2 = max(np.abs(all_offset).sum(1))
    
    print("Part 1 —", part1)
    print("Part 2 —", part2)
    
