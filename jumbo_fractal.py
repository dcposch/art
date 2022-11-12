import random_walk_no_touch
import random_walk_hex
import frame
import common
import random
from pyaxidraw import axidraw


def rw(ad, b, type):
    step = 0.08
    small_b = b.inset(step)
    if small_b.w > 0 and small_b.h > 0:
        if type == 0:
            random_walk_no_touch.draw_random_walk(ad, small_b, step)
        else:
            random_walk_hex.draw_random_walk(ad, small_b, step)
    frame.draw_frame(ad, b)


def draw(ad):
    w, h, m = 33, 23, 1  # paper dimensions and margin, in inches
    g = 0.1  # gap, inches
    max_a = 40  # square inches

    b = common.Bounds([m, w-m], [m - 0.125, h-m-0.125])
    bounds = []
    subdivide(b, g, max_a, bounds)

    # Skip most boxes for paint-over
    skip = True

    print("Drawing jumbo nested random walks")
    types = list(map(lambda _: int(random.random() * 2), bounds))
    is_skipping = True
    for i, box in enumerate(bounds):
        if is_skipping and random.random() < 0.2:
            is_skipping = False
        elif not is_skipping and random.random() < 0.3:
            is_skipping = True
        if is_skipping:
            continue
        print("Drawing box %r, %d / %d" % (box, i, len(bounds)))
        rw(ad, box, types[i])

    print("Done")


def subdivide(b, g, max_a, bounds):
    # base case, decide whether bound b is a leaf
    frac = (b.w * b.h) / max_a
    if random.random() > frac:  # never hits if area > max area, frac > 1
        bounds.append(b)
        return

    # split bound b in half, randomly
    split = 0.1 + random.random() * 0.8
    b1, b2 = None, None
    if b.w > b.h:
        split_x = b.x[0] + b.w*split
        b1 = common.Bounds([split_x + g/2, b.x[1]], b.y)
        b2 = common.Bounds([b.x[0], split_x - g/2], b.y)
    else:
        split_y = b.y[0] + b.h * split
        b1 = common.Bounds(b.x, [split_y + g/2, b.y[1]])
        b2 = common.Bounds(b.x, [b.y[0], split_y - g/2])
    subdivide(b1, g, max_a, bounds)
    subdivide(b2, g, max_a, bounds)


def init(ad: axidraw.AxiDraw):
    print("Initializing jumbo plot")
    ad.options.pen_pos_down = 40
    ad.options.pen_pos_up = 70
    ad.options.const_speed = True
    ad.options.model = 5  # SE A1 jumbo plotter


def main():
    common.safe_plot_seeds(draw, init)


if __name__ == "__main__":
    main()
