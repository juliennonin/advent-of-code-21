# %%
def decode_entry(line):
    T = [0] * 10
    fivers, sixers = [], []
    map_unique_size = {2: 1, 3: 7, 4: 4, 7: 8}
    for c in line:
        c = frozenset(c)
        n = len(c)
        if n in map_unique_size:
            T[map_unique_size[n]] = c
        elif n == 5:
            fivers.append(c)
        elif n == 6:
            sixers.append(c)

    cde = T[8] - frozenset.intersection(*sixers)
    cf = T[1] & T[7]
    c = cde & cf
    f = cf - c  # cf & ~ c

    for x in fivers:
        if not f.issubset(x):
            T[2] = x
        elif not c.issubset(x):
            T[5] = x
        else:
            T[3] = x

    e = T[2] - T[3]

    for x in sixers:
        if not c.issubset(x):
            T[6] = x
        elif not e.issubset(x):
            T[9] = x
        else:
            T[0] = x

    return dict(zip(T, range(10)))

# %%
if __name__ == "__main__":
    with open("../data/day08.txt", "r") as f:
        data = [line.replace(' | ', ' ').split(' ') for line in f.read().splitlines()]

    part1, part2 = 0, 0
    for line in data:
        entry, output =  line[:-4], line[-4:]
        part1 += len([1 for num in output if len(num) in [2, 3, 4, 7]])
        decode = decode_entry(entry)
        output_digits = map(decode.get, map(frozenset, output))
        part2 += sum([n * 10 ** (3 - i) for i, n in enumerate(output_digits)])

    print("Part 1 —", part1)
    print("Part 2 —", part2)
