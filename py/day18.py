# %%
from enum import Enum
from copy import deepcopy

class Side(Enum):
    LEFT = 0
    RIGHT = 1

# %%
class SnailNode():
    def __init__(self):
        self.parent = None
        self.side = None

    def replace(self, other):
        if self.parent is None:
            return other
        if self.side is Side.RIGHT:
            self.parent.right = other
        elif self.side is Side.LEFT:
            self.parent.left = other
        other.side = self.side
        self.side = None
        other.parent = self.parent
        self.parent._update_depth()
        self._depth = 1
        self.parent = None
        return other

    @property
    def depth(self):
        raise NotImplementedError
    
    @property
    def magnitude(self):
        raise NotImplementedError

    def get_left_most(self):
        raise NotImplementedError
    
    def get_right_most(self):
        raise NotImplementedError
    
    def get_too_big(self):
        raise NotImplementedError


class Literal(SnailNode):
    def __init__(self, n):
        assert isinstance(n, int)
        self.val = n
        super().__init__()
    
    @property
    def depth(self):
        return 0

    @property
    def magnitude(self):
        return self.val

    def get_left_most(self):
        return self
    
    def get_right_most(self):
        return self

    def get_too_big(self):
        return self if self.val > 9 else None

    def split(self):
        a = self.val // 2
        b = self.val - a
        pair = SnailNb(a, b)
        return self.replace(pair)
    
    def __add__(self, other):
        if isinstance(other, Literal):
            return Literal(self.val + other.val)
        else:
            return Literal(self.val + other)

    def __iadd__(self, other):
        if isinstance(other, Literal):
            self.val += other.val
        else:
            self.val += other
        return self

    def __gt__(self, other):
        if isinstance(other, Literal):
            return self.val > other.val
        return self.val > other

    def __repr__(self):
        return f"{self.val}"


class SnailNb(SnailNode):
    def __init__(self, left, right):
        self.left = SnailNb._convert_value(left)
        self.left.parent = self
        self.left.side = Side.LEFT

        self.right = SnailNb._convert_value(right)
        self.right.parent = self
        self.right.side = Side.RIGHT

        super().__init__()
        self._depth = 1 + max(self.right.depth, self.left.depth)
    
    def _convert_value(val):
        if isinstance(val, int):
            return Literal(val)
        elif isinstance(val, SnailNb) or isinstance(val, Literal):
            return val
        else:
            raise TypeError
    
    def reduce(self):
        if self._depth > 4:
            self._explode()
        elif (big := self.get_too_big()) is not None:
            big.split()
        else:
            return self
        self.reduce()

    def create_from_list(L):
        if isinstance(L, int):
            return Literal(L)
        elif isinstance(L, list):
            assert len(L) == 2 
            return SnailNb(SnailNb.create_from_list(L[0]), SnailNb.create_from_list(L[1]))
        else:
            raise TypeError

    @property
    def depth(self):
        return self._depth
    
    @property
    def magnitude(self):
        return 3 * self.left.magnitude + 2 * self.right.magnitude


    def get_left_most(self):
        if self.depth == 1:
            return self.left
        else:
            return self.left.get_left_most()

    def get_right_most(self):
        if self.depth == 1:
            return self.right
        else:
            return self.right.get_right_most()

    def get_deepest(self):
        if self.depth == 1:
            return self
        if self.left.depth == self.depth - 1:
            return self.left.get_deepest()
        return self.right.get_deepest()
    
    def get_too_big(self):
        return self.left.get_too_big() or self.right.get_too_big()

    def get_right_siblings(self):
        t = self
        while t.side is Side.RIGHT:
            t = t.parent
        if t.side is None:
            return None
        return t.parent.right.get_left_most()
    
    def get_left_siblings(self):
        t = self
        while t.side is Side.LEFT:
            t = t.parent
        if t.side is None:
            return None
        return t.parent.left.get_right_most()

    def _explode(self):
        exploding_pair = self.get_deepest()
        right_sibl = exploding_pair.get_right_siblings()
        left_sibl = exploding_pair.get_left_siblings()
        if right_sibl is not None:
            right_sibl.__iadd__(exploding_pair.right)
        if left_sibl is not None:
            left_sibl.__iadd__(exploding_pair.left)
        exploding_pair.replace(Literal(0))

    def _update_depth(self):
        new_depth = 1 + max(self.right.depth, self.left.depth)
        if new_depth != self._depth:
            self._depth = new_depth
            if self.parent is not None:
                self.parent._update_depth()

    def __add__(self, other):
        res = SnailNb(deepcopy(self), deepcopy(other))
        res.reduce()
        return res

    def __radd__(self, other):
        if isinstance(other, int):
            if other == 0:
                return self
            raise ValueError
        raise TypeError

    def __repr__(self):
        return f"[{self.left},{self.right}]"

# %%
if __name__ == "__main__":
    with open("../data/day18.txt", "r") as f:
        nbs = [SnailNb.create_from_list(eval(line)) for line in f.read().splitlines()]

    part1 = sum(nbs).magnitude
    part2 = max((x + y).magnitude for x in nbs for y in nbs if x != y)

    print("Part 1 —", part1)
    print("Part 2 —", part2)

