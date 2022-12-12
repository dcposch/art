import common
from pyaxidraw import axidraw
import argparse


def draw(ad: axidraw.AxiDraw, b: common.Bounds):
    common.movep(ad, b.loc(0, 0))
    common.linep(ad, b.loc(0*b.w, 1*b.h))
    common.linep(ad, b.loc(1*b.w, 1*b.h))
    common.linep(ad, b.loc(1*b.w, 0*b.h))
    common.linep(ad, b.loc(0*b.w, 0*b.h))


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 45
    ad.options.pen_pos_up = 55
    ad.options.pen_down_speed = 50
    ad.options.pen_up_speed = 90
    ad.options.const_speed = True
    ad.options.model = 5  # SE A1 jumbo plotter


if __name__ == "__main__":
    parser = argparse.ArgumentParser('rect')
    parser.add_argument('xo', type=float, help='Left x, in inches')
    parser.add_argument('yo', type=float, help='Top y, in inches')
    parser.add_argument('w', type=float, help='Width in inches')
    parser.add_argument('h', type=float, help='Height in inches')
    args = parser.parse_args()

    b = common.Bounds((args.xo, args.xo+args.w), (args.yo, args.yo+args.h))

    common.safe_plot(lambda ad: draw(ad, b), init)
