import common
from pyaxidraw import axidraw
import math
import argparse
import random

P = tuple[float, float]


class WarpedBounds(common.Bounds):
    def __init__(self, x: P, y: P, d: P):
        common.Bounds.__init__(self, x, y, d)

    def loc(self, x, y) -> tuple[float, float]:
        xf = (x*self.dx)/self.w
        yf = (y*self.dy)/self.h
        yspread = yf*yf + yf + 1  # range 1-3

        u, v = super().loc(x, y)  # in inches
        v += ((xf * xf) * 0.5 + 0.15 * (math.cos(xf * 2 * math.pi) - 1))*yspread
        u += (yf * yf) * 0.3
        return (u, v)


def draw(ad: axidraw.AxiDraw, xo: float, yo: float, dim: float, depth: int, style: str):
    pix = 3**depth  # in pixels
    dx = (dim)/pix  # inches per pixel
    # b = WarpedBounds([xo, dim+xo], [yo, dim+yo], [dx, dx])
    b = common.Bounds((xo, dim+xo), (yo, dim+yo), (dx, dx))
    print("Drawing %dx%d sierpinski carpet at %r, %s" % (pix, pix, b, style))
    draw_rec(ad, 0, 0, b, depth, False, style, 0)

    print("Done")


strokes_since_dip = 1e9


def draw_rec(ad: axidraw.AxiDraw, i0: int, j0: int, b: common.Bounds, depth: int, black: bool, style: str, dir: int):
    if black and style == 'circles':
        r = float(3**depth) / 2
        c = (float(i0)+r, float(j0)+r)
        for ri in range(1, 3**depth + 1):
            if ri % 2 == 1:
                draw_circle(ad, ri/2, c, b)
        return

    if depth == 0 and black and style == 'points':
        c = (float(i0)+0.5, float(j0)+0.5)
        ad.penup()
        draw_circle(ad, 0.25, c, b)

    if depth == 0 and black and style == 'strokes':
        global strokes_since_dip
        if random.random() < 0.1 or strokes_since_dip > 10:
            # Dip pen in the central square. To prepare, sketch it using
            # depth=1 rectangle, then manually fill the central square w paint.
            sixth = int(round(b.w/b.dx))/6
            middle_s = int(2.5*sixth)
            ic, jc = (i0 % sixth) + middle_s, (j0 % sixth) + middle_s
            ad.penup()
            common.movep(ad, b.loc(float(ic)+0.5, float(jc)+0))
            common.linep(ad, b.loc(float(ic)+0.5, float(jc)+1))
            strokes_since_dip = 0
        strokes_since_dip += 1

        ad.penup()
        common.movep(ad, b.loc(float(i0)+0.5, float(j0)+0))
        common.linep(ad, b.loc(float(i0)+0.5, float(j0)+1))

    if depth == 0 and black and style == 'squiggle':
        common.line_or_movep(ad, b.loc(float(i0)+0.5, float(j0)+0.5))

    if depth == 0 and black and style == 'squiggler':
        fx, fy = b.abs_to_01(b.loc(float(i0), float(j0)))
        amp = math.sin(fx * fy * math.pi)
        rx = (1-amp)/2 + random.random()*amp
        ry = (1-amp)/2 + random.random()*amp
        common.line_or_movep(ad, b.loc(float(i0)+rx, float(j0)+ry))

    if depth == 0 and black and style == 'squares':
        frac = 0.6
        f1 = (1 - frac) / 2
        f2 = 1 - f1
        common.movep(ad, b.loc(float(i0)+f1, float(j0+f1)))
        common.linep(ad, b.loc(float(i0)+f1, float(j0+f2)))
        common.linep(ad, b.loc(float(i0)+f2, float(j0+f2)))
        common.linep(ad, b.loc(float(i0)+f2, float(j0+f1)))
        common.linep(ad, b.loc(float(i0)+f1, float(j0+f1)))

    if depth == 0:
        return

    # recurse 9x
    off = 3**(depth-1)

    dirs_table = [
        # Up right, 00 to 22
        [(0, 0, 0), (1, 0, 2), (2, 0, 0),
         (2, 1, 1), (1, 1, 3), (0, 1, 1),
         (0, 2, 0), (1, 2, 2), (2, 2, 0)],
        # Up left, 20 to 02
        [(2, 0, 1), (1, 0, 3), (0, 0, 1),
         (0, 1, 0), (1, 1, 2), (2, 1, 0),
         (2, 2, 1), (1, 2, 3), (0, 2, 1)],
        # Down right, 02 to 20
        [(0, 2, 2), (1, 2, 0), (2, 2, 2),
         (2, 1, 3), (1, 1, 1), (0, 1, 3),
         (0, 0, 2), (1, 0, 0), (2, 0, 2)],
        # Down left, 22 to 00
        [(2, 2, 3), (1, 2, 1), (0, 2, 3),
         (0, 1, 2), (1, 1, 0), (2, 1, 2),
         (2, 0, 3), (1, 0, 1), (0, 0, 3)],
    ]
    dirs = dirs_table[dir]
    for (subi, subj, subdir) in dirs:
        middle = subi == 1 and subj == 1
        subx, suby = i0+subi*off, j0+subj*off
        draw_rec(ad, subx, suby, b, depth-1, middle or black, style, subdir)


def draw_circle(ad: axidraw.AxiDraw, r: float, c: tuple[float, float], b: common.Bounds):
    ad.penup()
    n = int(20*r + 1)
    for i in range(n + 1):
        x = c[0] + r * math.cos(2 * math.pi * i / n)
        y = c[1] + r * math.sin(2 * math.pi * i / n)
        l = b.loc(x, y)
        common.line_or_movep(ad, l)


def init(ad: axidraw.AxiDraw, style: str):
    if style == 'strokes':
        # Paint
        ad.options.pen_pos_down = 30
        ad.options.pen_pos_up = 70
    else:
        # Pen or marker
        ad.options.pen_pos_down = 45
        ad.options.pen_pos_up = 55
    ad.options.pen_down_speed = 30
    ad.options.pen_up_speed = 90
    ad.options.const_speed = True
    # ad.options.model = 5  # SE A1 jumbo plotter


if __name__ == "__main__":
    parser = argparse.ArgumentParser('sierpinski')
    parser.add_argument('xo', type=float, help='Left x, in inches')
    parser.add_argument('yo', type=float, help='Top y, in inches')
    parser.add_argument('dim', type=float, help='Width in inches')
    parser.add_argument('depth', type=int,
                        help='Fractal depth d, 3**d px across')
    parser.add_argument(
        'style', choices=['circles', 'points', 'squares', 'squiggle', 'squiggler', 'strokes'])
    parser.add_argument(
        'skip', type=int, default=0, help='Moves to skip', nargs='?')
    parser.add_argument('--name', type=str, help='Device name', default='')
    args = parser.parse_args()
    common.skip(args.skip)
    common.safe_plot(lambda ad: draw(ad, args.xo, args.yo,
                     args.dim, args.depth, args.style),
                     lambda ad: init(ad, args.style),
                     args.name)
