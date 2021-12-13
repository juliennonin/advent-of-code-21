# %%
import numpy as np
import matplotlib.pyplot as plt

# %% parsing & utils
def parse_dots(data_dots):
    return set(map(
        lambda s: tuple(map(int, s.split(','))),
        data_dots
    ))

def parse_instruction(instruction):
    axis, thresh = instruction.removeprefix("fold along ").split("=")
    axis = 0 if axis == "x" else 1
    return int(thresh), axis

def save_paper_svg(paper_set, filename):
    max_x = max(coords[0] for coords in paper_set)
    max_y = max(coords[1] for coords in paper_set)
    paper = np.zeros((max_y + 1, max_x + 1), dtype=bool)
    for x, y in paper_set:
        paper[y, x] = True
    plt.imshow(paper, cmap="gray_r")
    plt.axis("off")
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# %% foldings
def fold_along_axis(coords, thresh, axis):
    x, y = coords
    if coords[axis] <= thresh:
        return (x, y)
    elif axis == 0:
        return (2 * thresh - x, y)
    else:
        return (x, 2 * thresh - y)

def folding_func(thresh, axis):
    return lambda coords: fold_along_axis(coords, thresh, axis)

# %%
if __name__ == "__main__":
    with open("../data/day13.txt", "r") as f:
        data = f.read()
        data_dots, instructions = data.split("\n\n")
        data_dots = data_dots.splitlines()
        instructions = map(parse_instruction, instructions.splitlines())
    
    paper = parse_dots(data_dots)
    for i, (thresh, axis) in enumerate(instructions):
        paper = map(folding_func(thresh, axis), paper)
        if i == 0:
            paper = set(paper)
            part1 = len(paper)
    paper = set(paper)
    path = "../img/day13.svg"
    save_paper_svg(paper, path)

    print("Part 1 —", part1)
    print(f"Part 2 — cf. '{path}'")

