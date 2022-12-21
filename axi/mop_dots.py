import math
import common
from pyaxidraw import axidraw
import argparse
import random


def gen_dots(b: common.Bounds, dpi: float):
    dots = []
    dim = max([b.w, b.h])
    n = math.floor(dim**2*dpi)
    print("Generating dots. Initial n=%d" % n)
    for _ in range(n):
        x, y = dim*random.random(), dim*random.random()
        p = sun(x, y, b.w, b.h)
        if random.random() > p:
            continue
        d = b.loc(x, y)
        if not d in b:
            continue
        dots.append(d)
    return dots


def sort_dots(dots: list[tuple[float, float]]):
    """Sort on a space-filling curve"""
    print("Sorting %d dots" % len(dots))
    return sort_dots_rec(dots, (0, 256), (0, 256), 0)


def sort_dots_rec(dots: list[tuple[float, float]], x: tuple[float, float], y: tuple[float, float], dir: int):
    if len(dots) <= 1:
        return dots  # Sorted

    # Dir 0 to 3 = up, right, down, left
    box0, box1 = None, None
    if dir == 0:
        pivot = sum(y) / 2
        box0, box1 = (x, (pivot, y[1])), (x, (y[0], pivot))
    elif dir == 1:
        pivot = sum(x) / 2
        box0, box1 = ((x[0], pivot), y), ((pivot, x[1]), y)
    elif dir == 2:
        pivot = sum(y) / 2
        box0, box1 = (x, (y[0], pivot)), (x, (pivot, y[1]))
    else:
        pivot = sum(x) / 2
        box0, box1 = ((pivot, x[1]), y), ((x[0], pivot), y)

    x0, y0 = box0
    x1, y1 = box1

    def is0(d: tuple[float, float]):
        return d[0] >= x0[0] and d[0] < x0[1] and d[1] >= y0[0] and d[1] < y0[1]

    dots0 = list(filter(is0, dots))
    dots1 = list(filter(lambda d: not is0(d), dots))
    d0, d1 = (dir + 1) % 4, (dir + 3) % 4

    return sort_dots_rec(dots0, x0, y0, d0) + sort_dots_rec(dots1, x1, y1, d1)


def draw_dots(ad: axidraw.AxiDraw, dots: list[tuple[float, float]]):
    print("Plotting %d dots" % len(dots))
    for i, dot in enumerate(dots):
        if i % 10 == 0:
            print("%d / %d dots..." % (i, len(dots)))
        ad.penup()
        ad.movep(dot)
        ad.pendown()
    ad.penup()


def sun(x: float, y: float, w: float, h: float) -> float:
    xc, yc = x-w/2, y-h/2
    m = min(w, h)/2
    mult = 4*math.pi / (m**(1.5))
    return math.sin(mult * math.sqrt(xc**2+yc**2)**1.5)**2


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 40
    ad.options.pen_pos_up = 60
    ad.options.pen_rate_raise = 50
    ad.options.pen_rate_lower = 100
    ad.options.pen_delay_down = 500
    ad.options.model = 5  # SE A1 jumbo plotter


if __name__ == "__main__":
    parser = argparse.ArgumentParser('spiral')
    parser.add_argument('xo', type=float, help='Left x, in inches')
    parser.add_argument('yo', type=float, help='Top y, in inches')
    parser.add_argument('w', type=float, help='Width in inches')
    parser.add_argument('h', type=float, help='Height in inches')
    parser.add_argument('dpi', type=float, help='Max dots per square inch')
    parser.add_argument('--name', type=str, help='Device name', default='')
    args = parser.parse_args()

    b = common.Bounds((args.xo, args.xo+args.w), (args.yo, args.yo+args.h))
    dots = gen_dots(b, args.dpi)
    dots = list(filter(lambda d: d[0] > 12 or d[1] > 9, dots))
    dots = sort_dots(dots)

    common.safe_plot(lambda ad: draw_dots(ad, dots),
                     lambda ad: init(ad),
                     args.name)
