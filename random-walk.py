from re import S
from pyaxidraw import axidraw
import math
import random
import collections
import common

# Bounds for letter paper, in inches
margin = [0.5, 0.5]
bx = [margin[0], 12-margin[0]]
by = [margin[1], 9-margin[1]]

# Random walk step size
step = 0.1

w = (bx[1]-bx[0]-margin[0]*2)/step
h = (by[1]-by[0]-margin[1]*2)/step

# Initial location
x = w / 4
y = h / 2

# Number of steps
n = 10

def draw_random_walk(ad):
    print("Plotting a random walk, %d steps, step size %r in"%(n, step))
    visit_count = collections.defaultdict(lambda: 0)
    visit_count[(x, y)] = 1

    init_in = loc_in(x, y)
    ad.penup()
    ad.moveto(init_in[0], init_in[1])

    # Plot
    for i in range(n):
        if i % 100 == 0:
            print("Completed %d / %d, currently at %d %d"%(i, n, x, y))

        while True:
            nx, ny = move_rand(x, y)

            # Check bounds, don't go off paper
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue

            # Make it less likely we revisit a location
            n_visit = visit_count[(nx, ny)]
            if random.random() > 2**(-n_visit):
                continue # never if n_visit is 0, half the time if 1, 3/4 if 2, etc

            # Done, this is the next location
            x, y = nx, ny
            visit_count[(x, y)] += 1
            break

        l = loc_in(x, y)
        ad.lineto(l[0], l[1])

def loc_in(x, y):
    """Given x and y in grid coordinates, returns a location in inches."""
    return [
        bx[0] + margin[0] + step*x,
        by[0] + margin[1] + step*y
    ]

def move_rand(x, y):
    direction = random.randint(0, 3)
    if direction == 0:
        x += 1
    elif direction == 1:
        x -= 1
    elif direction == 2:
        y -= 1
    else:
        y += 1
    return (x, y)

safe_plot(draw_random_walk)
