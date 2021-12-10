# %%
from functools import reduce

# %%
OPENINGS, CLOSINGS = '([{<', ')]}>'
PAIRS = dict(zip(OPENINGS, CLOSINGS))
COST_ERRORS = dict(zip(CLOSINGS, [3, 57, 1197, 25137]))
COST_COMPLETION = dict(zip(CLOSINGS, [1, 2, 3, 4]))

# %%
def find_illegal_char(line):
    """
    Returns: 
        (char or False, str): illegal character or False & the completion string 
    """
    stack = ''
    for char in line:
        if char not in PAIRS:
            # expected = stack.pop() if len(stack) != 0 else False
            if len(stack) == 0 or stack[-1] != char:
                # print(f"Expected {expected}, but found {char} instead")
                return char, stack
            stack = stack[:-1]
        else:
            stack += PAIRS[char]
    return False, ''.join(stack[::-1])

# %%
if __name__ == "__main__":
    with open("../data/day10.txt", "r") as f:
        data = f.read().splitlines()
    
    score_errors, scores_completion = 0, []
    for line in data:
        illegal_char, autocomplete = find_illegal_char(line)
        if illegal_char:
            score_errors += COST_ERRORS[illegal_char]
        else:
            scores_completion.append(
                reduce(
                    lambda cost, char: 5 * cost + COST_COMPLETION[char],
                    autocomplete, 0)
            )
    scores_completion.sort()
    middle_score_completion = scores_completion[len(scores_completion) // 2]

    print("Part 1 —", score_errors)
    print("Part 2 —", middle_score_completion)