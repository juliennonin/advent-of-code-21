# %%
hallway = ['01234567']
rooms = ['D', 'C', 'D', 'B']
nexts = ['B', 'A', 'A', 'C'] 

# rooms[i] is connected to slots i+1 and i+2
L = [None] * 4
h = {0: '01234567', 1:'01234567', 2:'01234567', 3:'01234567', 4:'01234567', 5:'01234567', 6:'01234567', 7:'01234567'}

locked = [0, 2, 4, 6]
a = [None, 0, 1, 2, 3, None]  # rooms
n = len(locked)
for i in range(n-1):
    print(a[locked[i]:locked[i+1]], list(range(locked[i]+1, locked[i+1])))
# %%
def possible_move(s):
    L, rooms = [], []
    for i in range(7):
        if i not in s:
            rooms.append(i)
        else:
            rooms = []
        L.append(rooms)
    return L[1:-2]

def check_free_move(hi, rj, rooms, obstacles):
    if rooms[rj] is not None:
        return False
    return all(f not in obstacles for f in routes(hi, rj))
    
    
def routes(hi, rj):
    assert 0 <= rj <= 3
    assert 0 <= hi <= 6
    rj += 1
    if rj > hi:
        return list(range(hi+1, rj+1))
    else:
        return list(range(rj+1, hi))

amphipods_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
amphipods_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
obstacles = {}
rooms = ['B', 'C', 'B', 'D']
nexts = ['A', 'D', 'C', 'A']

def calc_cost(amphipod, hallway, room):
    distance = 1 + len(routes(hallway, room))
    return distance * amphipods_costs[amphipod]

ROOMS = "αβγδ"

def display(obstacles, rooms, nexts, shift=0):
    s = " "* shift
    s += obstacles.get(0, '.') +'.'.join(obstacles.get(i, '.') for i in range(1, 6)) + obstacles.get(6, '.') + "\n"
    s += " "* shift + "  " + ' '.join(c if c is not None else '.' for c in rooms) + "\n"
    s += " "* shift + "  " + ' '.join(c if c is not None else '.' for c in nexts)
    print(s)

def update(obstacles, rooms, nexts, room, hallway):
    obstacles = obstacles.copy()
    rooms = rooms.copy()
    nexts = nexts.copy()
    amphipod = rooms[room]
    obstacles[hallway] = amphipod
    rooms[room], nexts[room] = nexts[room], None
    return obstacles, rooms, nexts

def one_step(state, cost, n=0, index='0'):
    obstacles, rooms, nexts = state
    obstacles = obstacles.copy()
    rooms = rooms.copy()
    nexts = nexts.copy()
    # print("\n" + " " * n + index, cost)
    # display(obstacles, rooms, nexts, n)
    if not any(rooms):
        return cost
    for h, amphipod in obstacles.items():
        amphipod_house = amphipods_rooms[amphipod]
        if check_free_move(h, amphipod_house, rooms, obstacles):
            obstacles.pop(h)  # free this space
            add_cost = calc_cost(amphipod, h, amphipod_house)
            # print(" " * n + f"Free {amphipod}:  {h} -> {ROOMS[amphipod_house]}  ({add_cost}).")
            return one_step((obstacles, rooms, nexts), cost+add_cost, n+1, index+'F')
    
    L = possible_move(obstacles.keys())
    cost_min = 1e8
    M = 0
    for i in range(4):
        if M == 1:
            break
        amphipod = rooms[i]
        if amphipod is None:
            continue
        for h in L[i]:
            add_cost = calc_cost(amphipod, h, i)
            # print(" " * n + f"Move {amphipod}:  {ROOMS[i]} -> {h}   ({add_cost}).")
            if (c := one_step(update(obstacles, rooms, nexts, i, h), cost + add_cost, n+1, index+str(M))) < cost_min:
                cost_min = c
            M += 1
            if M == 2:
                break
    # print(index, cost_min)
    # if cost_min == 1e8:
    #     print(" " * n, "BLOCKED")
    return cost_min

one_step((obstacles, rooms, nexts), 0)


# %%
