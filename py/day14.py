# %%
def parse_template(tpl):
    pair, elmt = tpl.split(" -> ")
    return pair, elmt

with open("../data/day14_test.txt", "r") as f:
    data = f.read()
    polymer, templates = data.split("\n\n")
    templates = dict(map(parse_template, templates.splitlines()))
# %%
# i = 0
# polymer = polymer_start
# while i < len(polymer) - 1:
#     pair = polymer[i:i+2]
#     print(polymer[i:i+2])
#     i += 1
# %%
def rec(pair, i, last, templates=templates):
    rec.count += 1
    if i == 0 or pair not in templates:
        return pair if last else pair[1]
    if (pair, i) in rec.mem:
        res = rec.mem[(pair, i)]
        return res if last else res[1:]

    elmt = templates[pair]
    res = rec(pair[0] + elmt, i-1, last=True) + rec(elmt + pair[1], i-1, last=False)
    rec.mem[(pair, i)] = res
    return res if last else res[1:]
rec.mem = {}
rec.count = 0
rec.L = [0] * 11

def polymerization(polymer, n, templates=templates):
    s = ''
    for i in range(len(polymer) - 1):
        pair = polymer[i: i+2]
        s += rec(pair, n, last=(i == 0), templates=templates)
    return s

def count(polymer):
    return {c: polymer.count(c) for c in set(polymer)}

# %%
def rec_count(pair, i, counts, templates=templates):
    if i == 0 or pair not in templates:
        return counts
    elmt = templates[pair]
    counts[elmt] = counts.setdefault(elmt, 0) + 1
    rec_count(pair[0] + elmt, i-1, counts)
    rec_count(elmt + pair[1], i-1, counts)
    return counts
rec_count.mem = {}

def polymerization_count(polymer, n, templates=templates):
    counts = count(polymer)
    for i in range(len(polymer) - 1):
        pair = polymer[i: i+2]
        rec_count(pair, n, counts, templates=templates)
    return counts

# %%
polymer_end = polymerization(polymer, 10)
print(f"{len(rec.mem)} values saved through memoization,\n{rec.count} calls to rec function.")
c = count(polymer_end)
print(max(c.values()) - min(c.values()))
# %%
c = polymerization_count(polymer, 10)
print(max(c.values()) - min(c.values()))
# %%
