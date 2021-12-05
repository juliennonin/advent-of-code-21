# %%
from math import gcd

# %%
class IntLine:
    def __init__(self, x1, y1, x2, y2):
        self.x, self.y = int(x1), int(y1)
        Δx, Δy = x2 - self.x, y2 - self.y
        self.N = gcd(Δx, Δy)
        self.δx, self.δy = Δx // self.N, Δy // self.N
    
    def all_points(self):
        for i in range(self.N + 1):
            yield (self.x + i * self.δx, self.y + i * self.δy)

    @property
    def is_straight(self):
        return self.δx == 0 or self.δy == 0
    
    @property
    def end_point(self):
        return self.x + self.N * self.δx, self.y + self.N * self.δy

    def __repr__(self):
        x_end, y_end = self.end_point
        return f"IntLine({self.x}, {self.y} -> {x_end}, {y_end})"

# %%
def main(data, only_straight=True):
    board = {}
    for c in data:
        line = IntLine(*c)
        if only_straight and not line.is_straight:
            continue
        for x, y in line.all_points():
            board[(x, y)] = board.get((x, y), 0) + 1
    return board

# %%
if __name__ == "__main__":
    with open("../data/day05.txt", 'r') as f:
        data = [
            list(map(int, line.replace(' -> ', ',').split(',')))
            for line in f.read().splitlines() 
        ]
    
    board = main(data, only_straight=True)
    print("Part 1 —", len([n for n in board.values() if n >= 2]))
    board = main(data, only_straight=False)
    print("Part 2 —", len([n for n in board.values() if n >= 2]))

