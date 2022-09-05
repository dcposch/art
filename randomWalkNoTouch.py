import random
import collections
import common
import math


def draw_random_walk(ad, bounds, step):
    w = int(math.round((bounds.x[1]-bounds.x[0])/step))
    h = int(math.round((bounds.y[1]-bounds.y[0])/step))

    # Initial location
    x = w // 2
    y = h // 2

    # Number of steps
    n = w * h * 2 // 3

    print("Plotting a random walk, %d steps, step size %r in" % (n, step))
    visit_count = collections.defaultdict(lambda: 0)
    visit_count[(x, y)] = 1

    ad.penup()
    l0 = bounds.loc(step*x, step*y)
    ad.moveto(l0[0], l0[1])

    def flood_fill_reachable(nx, ny, nff):
        """Number of reachable unvisited squares flood-filling from nx, ny"""
        q = collections.deque()
        q.appendleft((nx, ny))
        filled = set()
        while len(q) > 0:
            p = q.pop()
            if p[0] < 0 or p[0] > w or p[1] < 0 or p[1] > h:
                continue
            if visit_count[p] > 0:
                continue
            if p in filled:
                continue

            # Found an unvisited point
            filled.add(p)
            if len(filled) >= nff:
                return True  # Filled nff unvisited points

            # Keep filling
            for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                q.appendleft((p[0]+dir[0], p[1]+dir[1]))

        # Did not find enough unvisited points
        return False

    # Plot
    for i in range(n):
        if i % 100 == 0:
            print("Completed %d / %d, currently at %d %d" % (i, n, x, y))

        successfully_stepped = False
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(dirs)
        for dir in dirs:
            nx, ny = (x + dir[0], y + dir[1])

            # Check bounds, don't go off paper
            if nx < 0 or ny < 0 or nx > w or ny > h:
                continue

            # Never revisit a location
            if visit_count[(nx, ny)] > 0:
                continue

            # Don't get stuck
            if not flood_fill_reachable(nx, ny, n-i):
                continue

            # Done, this is the next location
            x, y = nx, ny
            successfully_stepped = True
            break

        if not successfully_stepped:
            print("Stuck, exiting")
            break

        # Move to the next location
        visit_count[(x, y)] += 1
        l = bounds.loc(step*x, step*y)
        ad.lineto(l[0], l[1])


def main(ad):
    margin = 0.6
    draw_random_walk(ad, common.Bounds(
        [margin, 12-margin], [margin, 9-margin]),  0.1)


if __name__ == "__main__":
    common.safe_plot(main)
