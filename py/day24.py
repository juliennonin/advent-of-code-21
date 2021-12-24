# %%
INSTR_TEMPLATE = [
    'mul x 0', 'add x z', 'mod x 26', 'div z z_div',
    'add x a_value', 'eql x w', 'eql x 0', 'mul y 0', 'add y 25',
    'mul y x', 'add y 1', 'mul z y', 'mul y 0', 'add y w',
    'add y b_value','mul y x', 'add z y']

def parse_block(block):
    instructions = block.strip().split("\n")
    
    variables = []
    for instr, tpl in zip(instructions, INSTR_TEMPLATE):
        if instr != tpl:
            variables.append(int(instr[6:]))
    
    z_div, a, b = variables
    return z_div, a, b

def rebuild_monad_documentation(monad_instrs):
    assert len(monad_instrs) == 14
    remainders = []  # list of tuples (var index, remainder)
    conds = []  # list of tuples (bound_variable, free_variable, value_to_add)
    for i, block in enumerate(monad_instrs):
        z_div, a, b = parse_block(block)        
        match z_div:
            case 1:
                assert 9 < a < 26 - 9
                remainders.append((i, b))
                # print(f"{i:>2}.  z = 26z + i{i} + {b}")
            case 26:
                assert a < 0
                variable, rem = remainders.pop()
                conds.append((i, variable, rem + a))
                # print(f"{i:>2}.  i{i} = i{variable} {rem:+}")
            case _:
                raise ValueError
    return conds

def find_valid_number(conds, func):
    inp = [None] * 14
    for (frozen_var, free_var, const) in conds:
        assert inp[free_var] is None
        if const >= 0:
            inp[free_var] = func(range(1, 10 - const))
        else:
            inp[free_var] = func(range(-const + 1, 10))
        inp[frozen_var] = inp[free_var] + const
    return int(''.join(map(str, inp)))

# %%
if __name__ == "__main__":
    with open("../data/day24.txt", "r") as f:
        monad = f.read()
        monad_instrs = monad.replace("inp w", "\n").strip().split("\n\n")

    conditions = rebuild_monad_documentation(monad_instrs)
    part1 = find_valid_number(conditions, min)
    part2 = find_valid_number(conditions, max)

    print("Part 1 —", part1)
    print("Part 2 —", part2)
