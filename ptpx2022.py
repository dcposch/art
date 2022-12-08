import common
from pyaxidraw import axidraw
import rect
import random_walk_hex
import sierp


def draw(ad: axidraw.AxiDraw):
    bpaper = common.Bounds((0, 12), (0, 9))
    bounds = common.create_grid(bpaper, 2, 2, 0.5)
    for stage in range(2):
        if stage > 0:
            common.wait(ad, "CHANGE PENS, then press enter to continue...")
        for i, b in enumerate(bounds):
            print("Drawing %d / %d" % (i, len(bounds)))
            if stage == 0:
                rect.draw(ad, b)
                random_walk_hex.draw_random_walk(ad, b.inset(0.1), 0.08)
            elif stage == 1:
                common.wait(ad)
                b1 = b.inset(0.2)
                sierp.draw(ad, b1.x[0], b1.y[0], b1.h, 3, "squares")


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 45
    ad.options.pen_pos_up = 55
    ad.options.pen_down_speed = 50
    ad.options.pen_up_speed = 90
    ad.options.const_speed = True


if __name__ == "__main__":
    common.safe_plot(draw, init)
