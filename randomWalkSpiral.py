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
w2 = (bx[1]-bx[0])/step/2  # half width, in steps
h2 = (by[1]-by[0])/step/2  # half height


def draw_random_walk(ad):
    # Initial location = center of page.
    x, y = 0, 0

    # Number of steps
    n = 5000

    print("Plotting a random walk, %d steps, step size %r in" % (n, step))
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
            if nx < -w2 or ny < -h2 or nx >= w2 or ny >= h2:
                continue

            # Make it less likely we revisit a location
            n_visit = visit_count[(nx, ny)]
            if random.random() > 2**(-n_visit):
                continue  # never if n_visit is 0, 50% if 1, 75% if 2, etc

            # Less likely to walk backwards
            # At loc (x, y), the forward direction is (y, -x)
            fx, fy = y, -x
            dot = ((nx - x) * fx + (ny - y) * fy) / math.sqrt(fx**2+fy**2+9)
            if random.random() > (dot*0.25 + 0.75):
                continue

            # Done, this is the next location
            x, y = nx, ny
            visit_count[(x, y)] += 1
            break

        l = loc_in(x, y)
        ad.lineto(l[0], l[1])


def loc_in(x, y):
    """Given x and y in grid coordinates, returns a location in inches."""
    return [
        bx[0] + step*(x + w2),
        by[0] + step*(y + h2)
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


if __name__ == "__main__":
    common.safe_plot(draw_random_walk)
