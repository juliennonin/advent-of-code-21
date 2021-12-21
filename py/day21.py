# %%
from collections import defaultdict

# %%
def wrap(n, a=1, b=10):
    return (n - a) % (b - a + 1) + a

def determinist_roll(pos1, pos2):
    positions = [pos1 - 1, pos2 - 1]
    scores = [0, 0]
    n = 0
    die = 0
    while max(scores) < 1000:
        i = n % 2
        for _ in range(3):
            die = wrap(die + 1, 1, 100)
            positions[i] = positions[i] + die
        positions[i] %= 10
        scores[i] += positions[i] + 1
        n += 1
    return min(scores) * 3 * n

#%%
def new_roll(L):
    """
    Args:
        L (list): L[k-1] containts a dict(score -> n_score) that counts the number
            of possible scores knowing that the player is currently on space k

    Returns:
        T (list): updated L after one turn
    """
    MAX_SCORE = 21
    large_scores_counts = 0
    roll_outcomes = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]  # (sum of 3 dice, occurences)
    T = [defaultdict(int) for _ in range(10)]
    for pos, scores in enumerate(L, start=1):
        for roll, roll_counts in roll_outcomes:
            new_pos = wrap(pos + roll)
            for current_score, score_counts in scores.items():
                new_score = current_score + new_pos
                new_score_counts = score_counts * roll_counts
                if new_score >= MAX_SCORE:
                    large_scores_counts += new_score_counts
                else:
                    T[new_pos - 1][new_score] += score_counts * roll_counts
    return large_scores_counts, T

def play(initial_pos):
    """
    Args:
        initial_pos (int between 1 and 10): Initial position of the player

    Returns:
        W (list): W[n] is the number of universes where the score of
            the player becomes larger than 21 at the n-th move
        R (list): R[n] is the number of universes where the score of
            the player is till below than 21 after the n-th move
    """
    assert 1 <= initial_pos <= 10
    L = [defaultdict(int) for _ in range(10)]
    L[initial_pos - 1][0] = 1

    W = [0]
    R = [1]
    
    while R[-1] != 0:
        large_scores_counts, L = new_roll(L)
        W.append(large_scores_counts)
        R.append(27 * R[-1] - large_scores_counts)  # 27 times more universes
    return W, R

def compute_wins_number(pos1, pos2):
    W1, L1 = play(pos1)
    W2, L2 = play(pos2)
    n = min(len(W1), len(W2))
    s1, s2 = 0, 0 # number of wins of players 1 & 2
    for i in range(n-1):
        s1 += W1[i+1] * L2[i]
        s2 += W2[i] * L1[i]
    return s1, s2

# %%
if __name__ == "__main__":
    with open("../data/day21.txt") as f:
        pos1, pos2 = [int(line.split(': ')[1]) for line in f.read().split("\n")]

    part1 = determinist_roll(pos1, pos2)
    part2 = max(compute_wins_number(pos1, pos2))
    
    print("Part 1 —", part1)
    print("Part 2 —", part2)

