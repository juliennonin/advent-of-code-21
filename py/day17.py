# %%
import numpy as np
from math import ceil, floor

# %%
def display(L, xlim, ylim):
    xmin = min(xlim[0], min(x for x, _ in L))
    xmax = max(xlim[1], max(x for x, _ in L))
    ymin = min(ylim[0], min(y for _, y in L))
    ymax = max(ylim[1], max(y for _, y in L))
    Δy, Δx = ymax - ymin + 1, xmax - xmin + 1
    T = [['⋅'] * Δx for _ in range(Δy)]
    # print(xmax, ymax)
    for x in np.arange(xlim[0], xlim[1] + 1):
        for y in np.arange(ylim[0], ylim[1] + 1):
            T[ymax-y][x-xmin] = '×'
    for x, y in L:
        # print(y, ymax - y, Δy)
        T[ymax-y][x-xmin] = "■"
    # T[ymax-0][0-xmin] = "░"
    # with open("../data/output17.txt", "w+") as f:
        # f.write('\n'.join([''.join(t) for t in T]))
    print('\n'.join([''.join(t) for t in T]))

# %%
def compute(vx0, vy0, xlim, ylim):
    xmin, xmax = xlim
    ymin, ymax = ylim
    ẟx, ẟy = vx0, vy0
    x, y = 0, 0
    i = 0
    while x < xmin or y > ymax:
        x += ẟx
        y += ẟy
        ẟx = max(0, ẟx - 1)
        ẟy -= 1
        i += 1
    return x, y

def sy(y, vy0):
    return np.sqrt(- 2 * y + vy0**2 + vy0 + 0.25) - vy0 - 0.5



# vx0, vy0 = 17, 50
# xmin, xmax = 137, 171
# ymin, ymax = -98, -73
xmin, xmax = 20, 30
ymin, ymax = -10, -5
N = 0
T = []
xstart = ceil(np.sqrt(2 * xmin + 1/4) - 1/2)
# vy0 -> ymin, 100
# vx0 -> xstart, xmin
for vy0 in range(1, 100):
    print(vy0, "=>", sy(ymax, vy0), sy(ymin, vy0), floor(sy(ymin, vy0)) - ceil(sy(ymax, vy0)) >= 0)
    for vx0 in range(xstart, xmin):
        x, y = compute(vx0, vy0, (xmin, xmax), (ymin, ymax))
        # L = compute2(vx0, vy0, (xmin, xmax), (ymin, ymax))
        if (xmin <= x <= xmax) and (ymin <= y <= ymax):
            if vy0 > 0:
                T.append((vx0, vy0))
                print((vx0,vy0))
                # display(L, (xmin, xmax), (ymin, ymax))
            N += 1
# print(N + (ymax - ymin + 1) * (xmax - xmin + 1))
# %%
xmin, xmax = 8, 22
ymin, ymax = -22, -15
xlim, ylim = (xmin, xmax), (ymin, ymax)

def sy(y, vy0):
    return vy0 + 0.5 + np.sqrt((vy0 + .5)**2 - 2*y)

def sx(x, vx0):
    if vx0 > np.sqrt(2 * x + 0.25) - 0.5:
        return vx0 + 0.5 - np.sqrt((vx0 + .5) ** 2 - 2*x)
    return np.inf


def cond(x, vx0):
    return vx0 > np.sqrt(2 * x + 0.25) - 0.5

def compute2(vx0, vy0, xlim, ylim):
    xmin, xmax = xlim
    ymin, ymax = ylim
    ẟx, ẟy = vx0, vy0
    x, y = 0, 0
    L = [(x, y)]
    i = 0
    while y > ymin: #x < xmin or y > ymax:
        x += ẟx
        y += ẟy
        L.append((x, y))
        ẟx = max(0, ẟx - 1)
        ẟy -= 1
        i += 1
        n = i - (2 * vy0 + 1)
        # print(i, n, y, -n * vy0 - n * (n+1) // 2)
    return L
vx0, vy0 = 6, 14
L = compute2(vx0, vy0, xlim, ylim)
nymin, nymax = np.ceil(sy(ymax, vy0)), np.floor(sy(ymin, vy0))
print("y", sy(ymax, vy0), sy(ymin, vy0))
nxmin, nxmax = np.ceil(sx(xmin, vx0)), np.floor(sx(xmax, vx0))
nmin, nmax = max(nxmin, nymin), min(nxmax, nymax)
print(nmax - nmin >= 0)
display(L, xlim, ylim)

# %%
xmin, xmax = 137, 171
ymin, ymax = -98, -73

ystart, yend = ymax, -ymin # ymin -> -ymin - 1
xstart, xend = ceil(np.sqrt(2 * xmin + 0.25) - 0.5), xmin # -> xmax + 1

def land_in_zone(v, xlim, ylim):
    vx, vy = v
    xmin, xmax = xlim
    ymin, ymax = ylim
    nymin, nymax = np.ceil(sy(ymax, vy)), np.floor(sy(ymin, vy))
    nxmin, nxmax = np.ceil(sx(xmin, vx)), np.floor(sx(xmax, vx))
    nmin, nmax = max(nxmin, nymin), min(nxmax, nymax)
    return nmax >= nmin

i = 0
for x in range(xstart, xend):
    for y in range(ystart, yend):
        if land_in_zone((x, y), (xmin, xmax), (ymin, ymax)):
            print(x, y)
            i += 1
print(i + (ymax - ymin + 1) * (xmax - xmin + 1))
# %%
