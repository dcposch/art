import random_walk_no_touch
import random_walk_hex
import frame
import common
import random


def rw(ad, b, type):
    step = 0.1
    small_b = b.inset(step)
    if small_b.w > 0 and small_b.h > 0:
        if type == 0:
            random_walk_no_touch.draw_random_walk(ad, small_b, step)
        else:
            random_walk_hex.draw_random_walk(ad, small_b, step)
    frame.draw_frame(ad, b)


def main(ad):
    w, h, m = 12, 8.9, 0.5  # paper dimensions and margin, in inches
    b = common.Bounds([m, w-m], [m, h-m])

    g = 0.1  # gap, inches
    bounds = []
    for _ in range(8):
        split = 0.25 + random.random() * 0.5
        if b.w > b.h:
            split_x = b.x[0] + b.w*split
            bounds.append(common.Bounds([split_x + g/2, b.x[1]], b.y))
            b = common.Bounds([b.x[0], split_x - g/2], b.y)
        else:
            split_y = b.y[0] + b.h * split
            bounds.append(common.Bounds(b.x, [split_y + g/2, b.y[1]]))
            b = common.Bounds(b.x, [b.y[0], split_y - g/2])
    bounds.append(b)
    bounds.reverse()
    types = list(map(lambda _: int(random.random() * 2), bounds))
    for i, box in enumerate(bounds):
        print("Drawing box %r" % box)
        rw(ad, box, types[i])

    ad.penup()
    input("Switch pens, then hit enter to continue...")

    print("Continuing with second color")
    for i, box in enumerate(bounds):
        if random.random() < 0.5:
            continue
        box = box.offset(g/2, g/2)
        print("Drawing box %r" % box)
        rw(ad, box, types[i])

    print("Done")


if __name__ == "__main__":
    common.safe_plot(main)
