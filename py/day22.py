# %%
class Interval:
    def __init__(self, a, b):
        assert a < b
        self.a = a
        self.b = b

    @property
    def size(self):
        return self.b - self.a
    
    def isdisjoint(self, other):
        return other.b <= self.a or self.b <= other.a
    
    def __and__(self, other):
        if self.isdisjoint(other):
            return None
        a, b = max(self.a, other.a), min(self.b, other.b)
        return Interval(a, b)

    def clone(self):
        return Interval(self.a, self.b)

    def __sub__(self, other):
        if self.a < other.a < other.b < self.b:
            return [Interval(self.a, other.a), Interval(other.b, self.b)]
        inter = self.__and__(other)
        if inter is None:
            return [self.clone()]
        if self.a == inter.a and self.b == inter.b:
            return []
        if self.a == inter.a:
            return [Interval(inter.b, self.b)]
        if self.b == inter.b:
            return [Interval(self.a, inter.a)]
        raise NotImplementedError

    def __repr__(self):
        return f"({self.a},{self.b})"

    def __str__(self):
        return f"{self.a} -> {self.b}"


class Cuboid:
    DIM = 3
    def __init__(self, lims):
        assert len(lims) == self.DIM
        self.lims = []
        for lim in lims:
            self.lims.append(
                lim if isinstance(lim, Interval) else Interval(*lim)
            )

    def clone(self):
        return Cuboid(self.lims)
    
    @property
    def size(self):
        s = 1
        for interval in self.lims:
            s *= interval.size
        return s

    def _split_axis(self, split, axis):
        assert axis < Cuboid.DIM
        assert isinstance(split, Interval)

        left_overs = []
        for diff in self.lims[axis] - split:
            cuboid = self.clone()
            cuboid.lims[axis] = diff
            left_overs.append(cuboid)
        to_split = self.clone()
        to_split.lims[axis] = self.lims[axis] & split
        return  left_overs, to_split
    
    def isdisjoint(self, other):
        return any(self.lims[i].isdisjoint(other.lims[i]) for i in range(self.DIM))

    def split(self, other):
        if self.isdisjoint(other):
            return [self.clone()]
        leftovers = []
        to_split = self
        for ax in range(self.DIM):
            lefts, to_split = to_split._split_axis(other.lims[ax], ax)
            leftovers.extend(lefts)
        return leftovers

    def __repr__(self):
        return f"Cuboid({self.lims[0]!r},{self.lims[1]!r},{self.lims[2]!r})"
    
    def __str__(self):
        return f"x({self.lims[0]}) y({self.lims[1]}) z({self.lims[2]})"


# %%
def parse(step):
    ison, instr = step.split(' ')
    ison = (ison == "on")
    lims = []
    for t in instr.split(','):
        mmin, mmax = map(int, t[2:].split('..'))
        lims.append((mmin, mmax+1))
    return ison, Cuboid(lims)

def update_split_lit_cubes(lit_cubes, cube):
    L = []
    for c in lit_cubes:
        if c.isdisjoint(cube):
            L.append(c)
        else:
            L.extend(c.split(cube))
    return L

def reboot(reboot_data):
    lit_cubes = []
    for step in reboot_data:
        ison, cube = parse(step)
        lit_cubes = update_split_lit_cubes(lit_cubes, cube)
        if ison:
            lit_cubes.append(cube)
    return lit_cubes

# %%
if __name__ == "__main__":
    with open("../data/day22.txt", "r") as f:
        reboot_data = f.read().splitlines()

    universe = Cuboid([(-50, 50), (-50, 50), (-50, 50)])
    lit_cubes = reboot(reboot_data)

    part1 = sum(cube.size for cube in lit_cubes if not cube.isdisjoint(universe))
    part2 = sum(cube.size for cube in lit_cubes)

    print("Part 1 —", part1)
    print("Part 2 —", part2)
