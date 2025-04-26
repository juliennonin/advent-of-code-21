# %%
import numpy as np

# %%
with open("../data/day04.txt", "r") as f:
    tirage = list(map(int, f.readline().strip().split(',')))
    data = f.read().split('\n\n')
    # data = f.read().splitlines()
K = len(data)
#%%
boards = np.zeros((K, 5, 5), dtype=int)
for i, board in enumerate(data):
    board = board.strip().splitlines()
    board = [[int(e) for e in line.split(' ') if e.isnumeric()] for line in board]
    boards[i] = board
boards
# %%
d = [dict() for _ in range(K)]
for i in range(5):
    for j in range(5):
        for k in range(K):
            d[k][boards[k, i, j]] = (i, j)

chosen = np.zeros((K, 5, 5), dtype=bool)
for num in tirage:
    for k in range(K):
        if not num in d[k]:
            continue
        (i, j) = d[k].pop(num)
        chosen[k, i, j] = 1
        if chosen[k].sum(1)[i] == 5 or chosen[k].sum(0)[j] == 5:
            print("Stop")
            break
    else:
        continue
    break
    

print(num * (~chosen[k] * boards[k]).sum())
# %%
d = [dict() for _ in range(K)]
for i in range(5):
    for j in range(5):
        for k in range(K):
            d[k][boards[k, i, j]] = (i, j)

ks = set(range(K))
chosen = np.zeros((K, 5, 5), dtype=bool)
for num in tirage:
    print(num, len(ks))
    for k in ks.copy():
        if not num in d[k]:
            continue
        (i, j) = d[k].pop(num)
        chosen[k, i, j] = 1
        if chosen[k].sum(1)[i] == 5 or chosen[k].sum(0)[j] == 5:
            ks.remove(k)
    if len(ks) == 0:
        break
    
print()
print(num * (~chosen[k] * boards[k]).sum())
# %%
