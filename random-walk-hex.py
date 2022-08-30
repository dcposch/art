import math
import random
import collections
import common

# Bounds for letter paper, in inches
margin = [0.5, 0.5]
bx = [margin[0], 12-margin[0]]
by = [margin[1], 9-margin[1]]

# Random walk step size
step_x = 0.1
step_y = step_x * math.sqrt(3) / 2
w = math.floor((bx[1]-bx[0])/step_x)
h = math.floor((by[1]-by[0])/step_y)

# Hex coordinates
#
# x =     \1__/2    \4__/5       y = 3
#         /   \     /   \
# x = 0__/1    \3__/4    \6__/   y = 2
#        \     /   \     /   \
# x =     \1__/2    \4__/5       y = 1
#


def loc_in(x, y):
    """Given x and y in hex coordinates, returns a location in inches."""
    if y % 2 > 0:
        x += 0.5
    return [
        bx[0] + step_x*x,
        by[0] + step_y*y
    ]


def move_rand(x, y):
    xn = x % 6
    yn = y % 2

    case = xn - yn
    if case not in [0, 1, 3, 4]:
        raise Exception("%d %d not hex" % (x, y))

    direction = random.randint(0, 2)
    if direction == 0:
        x += 1 if case in [0, 3] else -1
    else:
        y += 1 if direction == 1 else -1
        if (xn, yn) in [(2, 1), (5, 1)]:
            x += 1
        if (xn, yn) in [(3, 0), (0, 0)]:
            x -= 1
    return (x, y)


def draw_random_walk(ad):
    # Initial location
    x = w / 4
    y = h / 2

    # Number of steps
    n = 5000

    print("Plotting a random walk, %d steps, step size %r in" % (n, step_x))
    visit_count = collections.defaultdict(lambda: 0)
    visit_count[(x, y)] = 1

    init_in = loc_in(x, y)
    ad.penup()
    ad.moveto(init_in[0], init_in[1])

    # Plot
    for i in range(n):
        if i % 100 == 0:
            print("Completed %d / %d, currently at %d %d" % (i, n, x, y))

        while True:
            nx, ny = move_rand(x, y)

            # Check bounds, don't go off paper
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue

            # Make it less likely we revisit a location
            n_visit = visit_count[(nx, ny)]
            if random.random() > 2**(-n_visit):
                continue  # never if n_visit is 0, 50% if 1, 75% if 2, etc

            # Done, this is the next location
            x, y = nx, ny
            visit_count[(x, y)] += 1
            break

        l = loc_in(x, y)
        ad.lineto(l[0], l[1])


common.safe_plot(draw_random_walk)
