# %%
import numpy as np

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
def roll_rows(A, shifts):
    """thanks @seberg https://stackoverflow.com/a/20361561/13410397"""
    n, m = A.shape
    shifts = np.array(shifts)
    assert shifts.ndim == 1 and n == len(shifts)
    rows, col_indices = np.ogrid[:n, :m]
    shifts[shifts < 0] += m
    col_indices = col_indices - shifts[:, np.newaxis]
    return A[rows, col_indices]

def roll_dice(A, N=3):
    for _ in range(N):
        A = np.roll(A, 1, axis=0) + np.roll(A, 2, axis=0) + np.roll(A, 3, axis=0)
    return A

def score_position(A):
    n, m = A.shape
    ## 1. Extract the scores that will be greater than m
    x, y = np.tril_indices(n)
    y = m - y - 1
    n_finished_games = np.sum(A[x, y])
    A[x, y] = 0
    ## 2. Add the current position to the current scores
    ## that is, shift each row nb k, k+1 steps to the right 
    A = roll_rows(A, np.arange(1, n+1))
    return A, n_finished_games

def play(initial_pos):
    """
    Args:
        initial_pos (int between 1 and 10): Initial position of the player

    Returns:
        W (list): W[n] is the number of universes where the score of
            the player becomes larger than 21 at the n-th move
        R (list): R[n] is the number of universes where the score of
            the player is still below than 21 after the n-th move
    """
    MAX_SCORE, N_ROLL, N_SPACE = 21, 3, 10
    
    A = np.zeros((N_SPACE, MAX_SCORE), dtype=int)
    # A[k, i] contains the number of scores i achievable at space k+1
    A[initial_pos - 1, 0] = 1
    W, R = [0], [1]
    while np.any(A):
        A = roll_dice(A, N_ROLL)
        A, w = score_position(A)
        W.append(w)
        R.append((3 ** N_ROLL) * R[-1] - w)
    return W, R

def compute_wins_number(pos1, pos2):
    W1, L1 = play(pos1)
    W2, L2 = play(pos2)
    n = min(len(W1), len(W2))
    s1, s2 = 0, 0 # number of wins of players 1 & 2
    for i in range(n - 1):
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

