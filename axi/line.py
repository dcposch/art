import common
from pyaxidraw import axidraw
import argparse


def draw(ad: axidraw.AxiDraw, a: tuple[float, float], b: tuple[float, float]):
    common.movep(ad, a)
    common.linep(ad, b)


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 45
    ad.options.pen_pos_up = 55
    ad.options.pen_down_speed = 50
    ad.options.pen_up_speed = 90
    ad.options.const_speed = True
    ad.options.model = 5  # SE A1 jumbo plotter


if __name__ == "__main__":
    parser = argparse.ArgumentParser('rect')
    parser.add_argument('x0', type=float, help='Start X, in inches')
    parser.add_argument('y0', type=float, help='Start Y, in inches')
    parser.add_argument('x1', type=float, help='End X, in inches')
    parser.add_argument('y1', type=float, help='End Y, in inches')
    args = parser.parse_args()

    a = (args.x0, args.y0)
    b = (args.x1, args.y1)
    common.safe_plot(lambda ad: draw(ad, a, b), init)
