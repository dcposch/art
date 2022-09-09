from pyaxidraw import axidraw
import traceback


class Bounds:
    """Contains x [min, max] and y [min, max] in inches."""

    def __init__(self, x, y):
        self.x = [x[0], x[1]]
        self.y = [y[0], y[1]]
        self.w = x[1]-x[0]
        self.h = y[1]-y[0]

    def __str__(self) -> str:
        return "[x:%r y:%r]" % (self.x, self.y)

    def __repr__(self) -> str:
        return self.__str__()

    def inset(self, l):
        x = self.x
        y = self.y
        return Bounds([x[0]+l, x[1]-l], [y[0]+l, y[1]-l])

    def offset(self, a, b):
        x = self.x
        y = self.y
        return Bounds([x[0]+a, x[1]+a], [y[0]+b, y[1]+b])

    def loc(self, x, y):
        ret = [x + self.x[0], y + self.y[0]]
        if x < 0 or y < 0 or ret[0] > self.x[1] or ret[1] > self.y[1]:
            raise Exception("%r out of bounds x%r y%r" % (ret, self.x, self.y))
        return ret

    def sub_bounds(self, x0, x1, y0, y1):
        ret = Bounds([self.x[0]+x0, self.x[0]+x1],
                     [self.y[0]+y0, self.y[0]+y1])
        if x0 < 0 or y0 < 0 or ret.x[1] > self.x[1] or ret.y[1] > self.y[1]:
            raise Exception("%r out of bounds %r" % (ret, self))
        return ret


def safe_plot(draw_func):
    # Set up
    print("Connecting to plotter...")
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.options.pen_pos_down = 10
    ad.options.pen_pos_up = 50
    ad.options.const_speed = True
    ad.connect()
    ad.penup()

    # Draw
    try:
        draw_func(ad)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    except KeyboardInterrupt:
        print("Interrupted, stopping...")

    # Move home
    print("Returning to home...")
    ad.penup()
    ad.moveto(0, 0)

    # Done, turn off
    print("Exiting, shutting off motors...")
    ad.disconnect()
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "disable_xy"
    ad.plot_run()


def lineto_or_moveto(ad, x, y):
    if ad.pen.status.pen_up:
        ad.moveto(x, y)
        ad.pendown()
    else:
        ad.lineto(x, y)
