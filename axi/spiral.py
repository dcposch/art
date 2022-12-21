import math
import common
from pyaxidraw import axidraw
import argparse


def draw_spiral(ad: axidraw.AxiDraw, b: common.Bounds):
    print("Plotting an oval spiral")
    # Center
    cx = sum(b.x) / 2
    cy = sum(b.y) / 2

    # Plot params
    r_offset = 0.325
    step_rad = 0.01
    in_per_rev = 0.4
    wobble_max_in = 0.15
    wobbles_per_in = 3

    diag = math.sqrt((cx-b.x[0])**2 + (cy-b.y[0])**2)
    num_revs = math.ceil(diag/in_per_rev)

    for i in range(math.floor(num_revs * 2 * math.pi / step_rad)):
        # Main spiral
        theta = i * step_rad
        r = r_offset + theta / (2 * math.pi) * in_per_rev
        x = cx + math.cos(theta) * r
        y = cy + math.sin(theta) * r

        # Add wobble for texture
        wobbliness = wobble_func(x, y)
        wobble_rho = i * step_rad * r * wobbles_per_in * 2 * math.pi
        wobble = math.sin(wobble_rho) * wobbliness * wobble_max_in
        x += math.cos(theta) * wobble
        y += math.sin(theta) * wobble

        if (x, y) in b:
            common.line_or_movep(ad, (x, y))
        else:
            ad.penup()


def wobble_func(x, y):
    """Given x and y in inches, returns a value between 0 (no wobble) and 1"""
    # 2D sine wave
    # return (0.5 + (math.sin(x * 3) * math.sin(y * 3)) / 2)**2

    # Curved waves
    return ((math.sin(y * 2 + y**2 / 20 + x**2 / 60) + 1) / 2)**2


if __name__ == "__main__":
    parser = argparse.ArgumentParser('spiral')
    parser.add_argument('xo', type=float, help='Left x, in inches')
    parser.add_argument('yo', type=float, help='Top y, in inches')
    parser.add_argument('w', type=float, help='Width in inches')
    parser.add_argument('h', type=float, help='Height in inches')
    parser.add_argument('--name', type=str, help='Device name', default='')
    args = parser.parse_args()

    b = common.Bounds((args.xo, args.xo+args.w), (args.yo, args.yo+args.h))

    common.safe_plot(lambda ad: draw_spiral(ad, b),
                     common.default_init,
                     args.name)
