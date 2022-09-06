import common
from frame import draw_frame


def draw_pixels(ad, bounds, px, gap, func):
    """Draws a bunch of px*px squares. 
    func(x,y) returns 0 (missing), 1 (empty), or 2 (filled)"""
    pg = px + gap
    w = int(bounds.w // pg)
    h = int(bounds.h // pg)
    for i in range(w):
        for j in range(h):
            val = func(i, j)
            if val == 0:
                continue

            box = bounds.sub_bounds(i*pg, i*pg + px, j*pg, j*pg + px)
            draw_frame(ad, box)
            if val == 1:
                continue
            if val != 2:
                raise Exception("Invalid bitmap %r at %d %d" % (val, i, j))

            # Lawnmower pattern fill
            pitch = 0.02
            for k in range(0, int(px//pitch), 2):
                ad.lineto(box.x[0] + k*pitch, box.y[0]+pitch)  # up
                ad.lineto(box.x[0] + k*pitch, box.y[1]-pitch)  # cross to right
                ad.lineto(box.x[0] + (k+1)*pitch, box.y[1]-pitch)  # up
                ad.lineto(box.x[0] + (k+1)*pitch, box.y[0]+pitch)  # cross


def main(ad):
    # Calc a few
    pixels = [
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 2, 2, 1, 0, 0],
        [0, 2, 1, 2, 1, 2, 0],
        [2, 1, 1, 2, 1, 2, 1]
    ]
    def func(x, y): return pixels[x][y]
    draw_pixels(ad, common.Bounds([1, 2.4], [3, 3.8]), 0.10, 0.04, func)


if __name__ == "__main__":
    common.safe_plot(main)
