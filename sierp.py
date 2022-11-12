import common
from pyaxidraw import axidraw
import imageio.v2 as imageio


def draw_pen(ad: axidraw.AxiDraw):
    print("Hello world")

    im = imageio.imread('./sierpinski/carpet.png')
    print("Read carpet, %dx%d pixels" % (im.shape))

    dim = 18  # in inches
    border = 0.5  # inches
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
            for j2 in range(pix):
                j = pix - j2 - 1 if i % 2 == 1 else j2
                pixel = 'o' if im[j][i] > 0 else ' '
                str += pixel
                if im[j][i] == 0:
                    continue

                y = j * dy
                frac = 0.75
                common.movep(ad, b.loc(x, y))
                common.linep(ad, b.loc(x, y+dy*frac))
                common.linep(ad, b.loc(x+dx*frac, y+dy*frac))
                common.linep(ad, b.loc(x+dx*frac, y))
                common.linep(ad, b.loc(x, y))

            print(str)
    print("Done")


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 25
    ad.options.pen_pos_up = 35
    ad.options.const_speed = True
    ad.options.model = 5  # SE A1 jumbo plotter


if __name__ == "__main__":
    common.safe_plot(draw_pen, init)
