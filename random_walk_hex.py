import math
from random import random, randint
import common


# Hex coordinates
#
# x =     \1__/2    \4__/5       y = 3
#         /   \     /   \
# x = 0__/1    \3__/4    \6__/   y = 2
#        \     /   \     /   \
# x =     \1__/2    \4__/5       y = 1
#


def move_rand(x, y):
    xn = x % 6
    yn = y % 2

    case = xn - yn
    if case not in [0, 1, 3, 4]:
        raise Exception("%d %d not hex" % (x, y))

    direction = randint(0, 2)
    if direction == 0:
        x += 1 if case in [0, 3] else -1
    else:
        y += 1 if direction == 1 else -1
        if (xn, yn) in [(2, 1), (5, 1)]:
            x += 1
        if (xn, yn) in [(3, 0), (0, 0)]:
            x -= 1
    return (x, y)


def is_hex(x, y):
    xn = x % 6
    yn = y % 2
    case = xn - yn
    return case in [0, 1, 3, 4]


def draw_random_walk(ad, bounds, step_x):
    # Random walk step size
    step_y = step_x * math.sqrt(3) / 2
    w = math.floor(bounds.w/step_x)
    h = math.floor(bounds.h/step_y)

    def loc_in(x, y):
        """Given x and y in hex coordinates, returns a location in inches."""
        if y % 2 > 0:
            x += 0.5
        return bounds.loc(x*step_x, y*step_y)

    visited = set()

    def pick_rand_unvisited():
        while True:
            p = (int(random() * w), int(random() * h))
            if is_hex(p[0], p[1]) and p not in visited:
                return p

    # Number of steps
    n = int(w * h * 0.4)
    print("Plotting a random walk, %d steps, step size %r in" % (n, step_x))

    def jump():
        nx, ny = pick_rand_unvisited()
        visited.add((nx, ny))
        nin = loc_in(nx, ny)
        ad.penup()
        ad.moveto(nin[0], nin[1])
        return nx, ny

    # Initial location
    x, y = jump()

    # Plot
    for i in range(n):
        if i % 100 == 0:
            print("Completed %d / %d, currently at %d %d" % (i, n, x, y))

        moved = False
        for _ in range(20):
            nx, ny = move_rand(x, y)

            # Check bounds, don't go off paper
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue

            # Make it less likely we revisit a location
            if (nx, ny) in visited:
                continue

            # Done, this is the next location
            x, y = nx, ny
            visited.add((x, y))
            moved = True
            break

        if not moved:
            print("Stuck, jumping")
            x, y = jump()

        l = loc_in(x, y)
        ad.lineto(l[0], l[1])


def main(ad):
    step = 0.08
    margin = 0.5
    w, h = 12, 8.9
    b = common.Bounds(
        [margin, w-margin], [margin, h-margin])
    draw_random_walk(ad, b, step)


if __name__ == "__main__":
    common.safe_plot(main)
