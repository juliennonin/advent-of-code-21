# %%
START, END = "start", "end"

def adjacency_map(data):
    """Transform the formatted input `data` into an adjacency map `adj`,
    Args:
        data (list of strs): each element is of the from A-B and
            represents an undirected link between A and B
    Returns:
        adj (dict of lists): adj[key] contains a list of nodes directly
            reachable from node key
    """
    adj = {}
    for line in data:
        node_a, node_b = line.split("-")
        adj.setdefault(node_a, []).append(node_b)
        adj.setdefault(node_b, []).append(node_a)
    return adj

def number_of_paths(cave, path, adj, can_visited_twice):
    """Recursively compute the number of paths from START to `cave`
    when the caves in `path` have already been visited

    Args:
        cave (node): current cave
        path (list of nodes): already visited caves (from the end)
        adj (dict [node]: list[nodes]): adjacency map of the cave system
        can_visited_twice (bool): True if a small cave can be visited twice,
                                  False otherwise
    """
    if cave.islower() and cave in path: 
        # this small cave has already been visited 
        if cave == END or not can_visited_twice:
            # it is not allowed anymore to visit a small cave twice
            return 0
        # now, other small caves are prevented from being visited more than once
        can_visited_twice = False 
    elif cave == START:
        # we found a path from the START!
        # print('start,'+','.join(reversed(path)))
        return 1
    
    new_path = path + [cave]
    n_paths_from_cave = 0
    for prev in adj[cave]:
        n_paths_from_cave += number_of_paths(prev, new_path, adj, can_visited_twice)
    return n_paths_from_cave

# %%
if __name__ == "__main__":
    with open("../data/day12.txt", "r") as f:
        data = f.read().splitlines()
    adj = adjacency_map(data)

    part1 = number_of_paths(END, [], adj, False)
    part2 = number_of_paths(END, [], adj, True)

    print("Part 1 —", part1)
    print("Part 2 —", part2)
