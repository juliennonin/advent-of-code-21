# %%
from collections import Counter, defaultdict

# %%
def parse_template(tpl):
    pair, elmt = tpl.split(" -> ")
    return pair, elmt

def count_pairs(polymer):
    n = len(polymer)
    counts = Counter(polymer[i: i+2] for i in range(n - 1))
    return defaultdict(int, counts)

def count_elements(pairs, first):
    counts = defaultdict(int, {first: 1})
    for pair, k in pairs.items():
        counts[pair[1]] += k
    return counts

# %%
def polymerize_once(pairs, templates):
    pairs_new = pairs.copy()
    for pair, k in pairs.items():
        if pair not in templates:
            continue
        # e.g. all SP become SN + NP
        pairs_new[pair] -= k
        elmt = templates[pair]
        pairs_new[pair[0] + elmt] += k
        pairs_new[elmt + pair[1]] += k
    return pairs_new

def main(polymer, n, templates):
    pairs = count_pairs(polymer)
    for _ in range(n):
        pairs = polymerize_once(pairs, templates)
    counts = count_elements(pairs, polymer[0])
    return max(counts.values()) - min(counts.values())

# %%
if __name__ == "__main__":
    with open("../data/day14.txt", "r") as f:
        data = f.read()
        polymer, templates = data.split("\n\n")
        templates = dict(map(parse_template, templates.splitlines()))

    part1 = main(polymer, 10, templates)
    part2 = main(polymer, 40, templates)

    print("Part 1 —", part1)
    print("Part 2 —", part2)

