# %%
import numpy as np

# %%
def minimum_vx(xmin):
    return np.sqrt(2 * xmin + 0.25) - 0.5

def ny_thresh(y, vy):
    return vy + 0.5 + np.sqrt((vy + .5)**2 - 2 * y)

def nx_thresh(x, vx):
    if vx <= minimum_vx(x):
        return np.inf
    return vx + 0.5 - np.sqrt((vx + .5)**2 - 2 * x)

def land_in_zone(v, xlim, ylim):
    (vx, vy), (xmin, xmax), (ymin, ymax) = v, xlim, ylim
    
    nymin, nymax = np.ceil(ny_thresh(ymax, vy)), np.floor(ny_thresh(ymin, vy))
    nxmin, nxmax = np.ceil(nx_thresh(xmin, vx)), np.floor(nx_thresh(xmax, vx))
    
    nmin, nmax = max(nxmin, nymin), min(nxmax, nymax)
    return nmax >= nmin

def count_correct_lauches(xlim, ylim):
    (xmin, xmax), (ymin, ymax) = xlim, ylim
    vy_range = (ymax, -ymin)
    vx_range = (int(np.ceil(minimum_vx(xmin))), xmin)
    
    count = (ymax - ymin + 1) * (xmax - xmin + 1)  # size of the landing zone
    for vx in range(*vx_range):
        for vy in range(*vy_range):
            if land_in_zone((vx, vy), xlim, ylim):
                count += 1
    return count

# %%
if __name__ == "__main__":
    with open("../data/day17.txt", "r") as f:
        line = f.read()
        instructions = line.removeprefix("target area:").strip().split(', ')
        xlim = tuple(map(int, instructions[0].removeprefix("x=").split("..")))
        ylim = tuple(map(int, instructions[1].removeprefix("y=").split("..")))

    ymin = ylim[0]
    part1 = ymin * (ymin + 1) // 2
    part2 = count_correct_lauches(xlim, ylim)

    print("Part 1 —", part1)
    print("Part 2 —", part2)

