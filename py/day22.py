# %%
import numpy as np
from enum import Enum

# %%
class Instruction:
    def __init__(self, ison, xlim, ylim, zlim):
        self.ison = ison
        self.xmin, self.xmax = xlim
        self.ymin, self.ymax = ylim
        self.zmin, self.zmax = zlim
    
    @property
    def lims(self):
        return [(self.xmin, self.xmax), (self.ymin, self.ymax), (self.zmin, self.zmax)]

    def slice(self, shift):
        S = []
        for mmin, mmax in self.lims:
            S.append(slice(mmin + shift, mmax + shift + 1))
        return tuple(S)

    def create_from_str(s):
        ison, instr = s.split(' ')
        ison = (ison == "on")
        lims = []
        for t in instr.split(','):
            mmin, mmax = map(int, t[2:].split('..'))
            lims.append((mmin, mmax))
        return Instruction(ison, *lims)

    def __repr__(self):
        return f"{int(self.ison)}| x({self.xmin:>4}, {self.xmax:>4}) y({self.ymin:>4}, {self.ymax:>4}) z({self.zmin:>4}, {self.zmax:>4})"

# %%
if __name__ == "__main__":
    with open("../data/day22.txt", "r") as f:
        data = f.read().splitlines()
        D = [Instruction.create_from_str(line) for line in data]

    N = 50
    size = 2 * N + 1  # from -N to +N
    A = np.zeros((size, size, size), dtype=bool)
    for instr in D:
        A[instr.slice(shift=N)] = instr.ison

    part1 = np.sum(A)

    print("Part 1 —", part1)
