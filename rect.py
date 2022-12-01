import common
from pyaxidraw import axidraw
import argparse


def draw(ad: axidraw.AxiDraw, xo: float, yo: float, w: float, h: float):
    common.movep(ad, [xo, yo])
    common.linep(ad, [xo + 0*w, yo + 1*h])
    common.linep(ad, [xo + 1*w, yo + 1*h])
    common.linep(ad, [xo + 1*w, yo + 0*h])
    common.linep(ad, [xo + 0*w, yo + 0*h])


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
    common.safe_plot(lambda ad: draw(
        ad, args.xo, args.yo, args.w, args.h), init)
