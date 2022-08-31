import random
import collections
import common


def draw_random_walk(ad, bounds, step):
    w = (bounds.x[1]-bounds.x[0])/step
    h = (bounds.y[1]-bounds.y[0])/step

    # Initial location
    x = w // 2
    y = h // 2

    # Number of steps
    n = int(w * h * 2 // 3)

    print("Plotting a random walk, %d steps, step size %r in" % (n, step))
    visit_count = collections.defaultdict(lambda: 0)
    visit_count[(x, y)] = 1

    ad.penup()
    l0 = bounds.loc(step*x, step*y)
    ad.moveto(l0[0], l0[1])

    # Plot
    for i in range(n):
        if i % 100 == 0:
            print("Completed %d / %d, currently at %d %d" % (i, n, x, y))

        successfully_stepped = False
        for j in range(40):
            nx, ny = move_rand(x, y)

            # Check bounds, don't go off paper
            if nx < 0 or ny < 0 or nx > w or ny > h:
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
            for j in range(100):
                if successfully_jumped:
                    break
                for k in range(4):
                    xd = (k % 2) * 2 - 1
                    yd = (k // 2) * 2-1
                    nx, ny = x+j*xd, y+j*yd
                    if nx < 0 or ny < 0 or nx > w or ny > h:
                        continue
                    if visit_count[(nx, ny)] > 0:
                        continue
                    print("Jumping from %d,%d to %d,%d" %
                          (x, y, nx, ny))
                    x, y = nx, ny
                    successfully_jumped = True
                    break

        if not successfully_stepped and not successfully_jumped:
            print("Stuck, exiting")
            break

        # Move to the next location
        visit_count[(x, y)] += 1
        l = bounds.loc(step*x, step*y)
        ad.lineto(l[0], l[1])


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


def main(ad):
    margin = 0.6
    draw_random_walk(ad, common.Bounds(
        [margin, 12-margin], [margin, 9-margin]),  0.1)


if __name__ == "__main__":
    common.safe_plot(main)
