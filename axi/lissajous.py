import math
import random
import common

# Bounds, in inches
margin = [0.5, 0.5]
bx = [margin[0], 12-margin[0]]
by = [margin[1], 9-margin[1]]


def to_pos(x, y):
    """Takes values in [-1, 1], returns values within bounds, in inches."""
    return [
        bx[0] + (bx[1]-bx[0]) * (x + 1)/2,
        by[0] + (by[1]-by[0]) * (y + 1)/2
    ]


def draw_lissajous(ad):
    p = [1, 1]
    jitter = 0
    print("Plotting a lissajous figure. Param %r, jitter %r" % (p, jitter))

    p0 = to_pos(1, 0)
    ad.penup()
    ad.moveto(p0[0], p0[1])
    step_rad = 0.05 / math.sqrt(p[0]**2 + p[1]**2)
    theta = 0
    while theta < 2 * math.pi:
        pn = to_pos(math.cos(theta*p[0]), math.sin(theta*p[1]))
        pn[0] += (random.random()*2-1) * jitter
        pn[1] += (random.random()*2-1) * jitter
        ad.lineto(pn[0], pn[1])
        theta += step_rad
    ad.lineto(p0[0], p0[1])
    print("Done")


if __name__ == "__main__":
    common.safe_plot(draw_lissajous)
