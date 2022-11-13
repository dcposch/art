import common
from pyaxidraw import axidraw
import imageio.v2 as imageio


def draw_pen(ad: axidraw.AxiDraw):
    print("Hello world")

    im = imageio.imread('./sierpinski/carpet.png')
    print("Read carpet, %dx%d pixels" % (im.shape))

    dim = 9  # in inches
    border = 0.5  # inches
    frac = 0.5  # width of each square / stride
    b = common.Bounds([border, dim-border], [border, dim-border])
    pix = 81  # in pixels
    dx, dy = b.w/pix, b.h/pix  # inches per pixel
    dry_run = False
    for i in range(pix):
        str = ""
        x = i * dx

        # dry run: just draw lines
        if dry_run:
            common.movep(ad, b.loc(x, 0))
            common.linep(ad, b.loc(x, b.h))
        else:
            was_down = False
            for j2 in range(pix):
                j = pix - j2 - 1 if i % 2 == 1 else j2
                pixel = 'o' if im[j][i] > 0 else ' '
                str += pixel
                if im[j][i] == 0:
                    was_down = False
                    continue

                y = j * dy
                if not was_down:
                    common.movep(ad, b.loc(x, y))
                common.linep(ad, b.loc(x, y+dy*frac))
                common.linep(ad, b.loc(x+dx*frac, y+dy*frac))
                common.linep(ad, b.loc(x+dx*frac, y))
                common.linep(ad, b.loc(x, y))
                was_down = True

            print(str)
    print("Done")


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 35
    ad.options.pen_pos_up = 50
    ad.options.pen_down_speed = 35
    ad.options.pen_up_speed = 90
    ad.options.const_speed = True
    ad.options.model = 5  # SE A1 jumbo plotter


if __name__ == "__main__":
    common.safe_plot(draw_pen, init)
