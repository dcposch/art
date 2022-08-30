import random
import collections
import common

# Bounds for letter paper, in inches
margin = [0.6, 0.6]
bx = [margin[0], 12-margin[0]]
by = [margin[1], 9-margin[1]]

# Random walk step size
step = 0.1
w = (bx[1]-bx[0])/step
h = (by[1]-by[0])/step


def draw_random_walk(ad):
    # Initial location
    x = w / 4
    y = h / 2

    # Number of steps
    n = 4000

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

        successfully_stepped = False
        for j in range(40):
            nx, ny = move_rand(x, y)

            # Check bounds, don't go off paper
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue

            # Never revisit a location
            if visit_count[(nx, ny)] > 0:
                continue

            # Done, this is the next location
            x, y = nx, ny
            successfully_stepped = True
            break

        # If we couldn't step, then jump
        successfully_jumped = False
        if not successfully_stepped:
            best_dist_2 = 1e99
            best_x, best_y = x, y
            for j in range(-20, 20, 1):
                for k in range(-20, 20, 1):
                    nx, ny = x+j, y+k
                    if nx < 0 or ny < 0 or nx >= w or ny >= h:
                        continue
                    if visit_count[(nx, ny)] > 0:
                        continue
                    dist_2 = (nx - x)**2 + (ny - y)**2
                    if dist_2 < best_dist_2:
                        best_dist_2 = dist_2
                        best_x, best_y = nx, ny
                        successfully_jumped = True
            if successfully_jumped:
                print("Jumping from %d,%d to %d,%d" % (x, y, best_x, best_y))
                x, y = best_x, best_y

        if not successfully_stepped and not successfully_jumped:
            print("Stuck, exiting")
            break

        # Move to the next location
        visit_count[(x, y)] += 1
        l = loc_in(x, y)
        ad.lineto(l[0], l[1])


def loc_in(x, y):
    """Given x and y in grid coordinates, returns a location in inches."""
    return [
        bx[0] + step*x,
        by[0] + step*y
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


common.safe_plot(draw_random_walk)
