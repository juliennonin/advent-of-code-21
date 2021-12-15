# %%
def part1(course):
    x, z = 0, 0
    for line in course:
        direction, step = line.split(' ')
        step = int(step)
        if direction == "forward":
            x += step
        elif direction == "down":
            z += step
        elif direction == "up":
            z -= step
    return x, z

# %%
def part2(course):
    x = z = a = 0
    for line in course:
        direction, step = line.split(' ')
        step = int(step)
        if direction == "down":
            a += step
        elif direction == "up":
            a -= step
        elif direction == "forward":
            x += step
            z += a * step
    return x, z

# %%
if __name__ == "__main__":
    with open("../data/day02.txt", 'r') as f:
        course = f.read().splitlines()

    x1, z1 = part1(course)
    print("Part 1 —", x1 * z1)
    x2, z2 = part2(course)
    print("Part 2 —", x2 * z2)

# %%
