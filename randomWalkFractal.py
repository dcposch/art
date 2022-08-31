import randomWalkJump
import frame
import common


def rw(ad, b):
    frame.draw_frame(ad, b)
    step = 0.1
    randomWalkJump.draw_random_walk(ad, b.inset(step), step)


def main(ad):
    m = 0.5  # margin, inches
    b = common.Bounds([m, 12-m], [m, 9-m])

    g = 0.2  # gap, inches
    bounds = []
    for _ in range(6):
        if b.w > b.h:
            bounds.append(common.Bounds([b.x[0]+b.w/2+g/2, b.x[1]], b.y))
            b = common.Bounds([b.x[0], b.x[0]+b.w/2-g/2], b.y)
        else:
            bounds.append(common.Bounds(b.x, [b.y[0] + b.h/2+g/2, b.y[1]]))
            b = common.Bounds(b.x, [b.y[0], b.y[0]+b.h/2-g/2])
    bounds.append(b)
    bounds.reverse()
    # Use this to paint over some boxes in a second color.
    # bounds = [bounds[0], bounds[3], bounds[6]]
    for box in bounds:
        rw(ad, box)


if __name__ == "__main__":
    common.safe_plot(main)
