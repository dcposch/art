import random
import collections
import common
import sys
import frame


def draw_random_walk(ad, bounds, step):
    w = int((bounds.x[1]-bounds.x[0])//step)
    h = int((bounds.y[1]-bounds.y[0])//step)

    # Initial location
    x = w // 2
    y = h // 2

    # Number of steps
    n = (w+1) * (h+1) * 1 // 2
    sys.setrecursionlimit(max(1000, n+10))
    print("Plotting a %dx%d random walk, %d steps @ %r in" % (w, h, n, step))

    # We want to generate a random space-filling curve.
    # This might be a computationally hard problem.
    # Approximate with a flood-fill heuristic and recursion.
    curve = []
    visited = set()
    assert gen_rand_fill(w//2, h//2, w, h, curve, visited, n)
    print("Generated a random space-filling curve of length %d" % len(curve))

    for i, point in enumerate(curve):
        x, y = bounds.loc(point[0]*step, point[1]*step)
        if i == 0:
            ad.penup()
            ad.moveto(x, y)
        else:
            ad.lineto(x, y)
        if i % 100 == 0:
            print("Completed %d / %d, currently at %d %d" % (i, n, x, y))


def gen_rand_fill(x, y, w, h, curve, visited, n):
    """Generate a random space-filling curve of length n, in [0, w] [0, h].
    Either succeeds, returning True and with the full curve listed in 'curve',
    or fails, returning False and leaving curve unmodified."""
    curve.append((x, y))
    visited.add((x, y))
    if n == 1:
        return True

    if random.random() < 0.01:
        print("Random sample @ %r, len(c) %d, (v) %d, n %d" %
              ((x, y), len(curve), len(visited), n))

    # Random walk to an unvisited neighboring grid point
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = map(lambda d: (x+d[0], y+d[1]), dirs)
    valid_next_locs = list(
        filter(lambda p: has_space(p[0], p[1], w, h, visited, n), neighbors))
    random.shuffle(valid_next_locs)

    # Limit recursive branching to allow deep backtrackings
    if len(valid_next_locs) > 1:
        max_rec = 1
        if random.random() < 8/(n+10):
            max_rec = 2
        valid_next_locs = valid_next_locs[:max_rec]

    for (nx, ny) in valid_next_locs:
        if gen_rand_fill(nx, ny, w, h, curve, visited, n - 1):
            return True

    curve.pop()
    visited.remove((x, y))
    return False


def has_space(x, y, w, h, visited, n):
    """Number of reachable unvisited squares flood-filling from nx, ny"""
    q = collections.deque()
    q.appendleft((x, y))
    filled = set()
    while len(q) > 0:
        p = q.pop()
        if p[0] < 0 or p[0] > w or p[1] < 0 or p[1] > h:
            continue
        if p in visited:
            continue
        if p in filled:
            continue

        # Found an unvisited point
        filled.add(p)
        if len(filled) >= n:
            return True  # Filled n unvisited points

        # Keep filling
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            q.appendleft((p[0]+dir[0], p[1]+dir[1]))

    # Did not find enough unvisited points
    return False


def main(ad):
    margin = 0.5
    w, h = 9, 7.9
    b = common.Bounds(
        [margin, w-margin], [margin, h-margin])
    frame.draw_frame(ad, b.inset(-0.1))
    draw_random_walk(ad, b, 0.1)


if __name__ == "__main__":
    common.safe_plot(main)
