from re import S
from pyaxidraw import axidraw
import math
import random
import common

ad = axidraw.AxiDraw()
ad.interactive()
ad.options.pen_pos_down = 10
ad.options.pen_pos_up = 30
ad.options.const_speed = True
ad.connect()

# Bounds for letter paper, in inches
margin = [2, 2]
bx = [margin[0], 11-margin[0]]
by = [margin[1], 8.5-margin[1]]


def to_pos(x, y):
    """Takes values in [-1, 1], returns values within bounds, in inches."""
    return [
        bx[0] + (bx[1]-bx[0]) * (x + 1)/2,
        by[0] + (by[1]-by[0]) * (y + 1)/2
    ]


# Lissajous
p = [1, 1]
jitter = 0
print("Plotting a lissajous figure. Param %r, jitter %r" % (p, jitter))

p0 = to_pos(1, 0)
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

ad.penup()
ad.moveto(0, 0)
ad.disconnect()
