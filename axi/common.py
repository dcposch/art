from time import sleep
from pyaxidraw import axidraw
import traceback
import typing
import random
import numpy as np


class Bounds:
    """Contains x [min, max] and y [min, max] in inches."""

    def __init__(self, x: tuple[float, float], y: tuple[float, float], d: tuple[float, float] = (1, 1)):
        self.x = [x[0], x[1]]
        self.y = [y[0], y[1]]
        self.w = x[1]-x[0]
        self.h = y[1]-y[0]
        self.dx = d[0]
        self.dy = d[1]

    def __str__(self) -> str:
        return "[x:%r y:%r]" % (self.x, self.y)

    def __repr__(self) -> str:
        return self.__str__()

    def __contains__(self, item: tuple[float, float]) -> bool:
        ix, iy = item
        x, y = self.x, self.y
        return ix >= x[0] and ix <= x[1] and iy >= y[0] and iy <= y[1]

    def inset(self, l: float):
        """Returns a new bounds, inset from the current bounds by l inches."""
        x = self.x
        y = self.y
        return Bounds([x[0]+l, x[1]-l], [y[0]+l, y[1]-l])

    def offset(self, a, b):
        x = self.x
        y = self.y
        return Bounds([x[0]+a, x[1]+a], [y[0]+b, y[1]+b])

    def loc(self, x, y) -> tuple[float, float]:
        """Given a relative point, returns a absolute point in inches."""
        ret = (x * self.dx + self.x[0], y * self.dy + self.y[0])
        # if x < 0 or y < 0 or ret[0] > self.x[1] or ret[1] > self.y[1]:
        #     raise Exception("%r out of bounds x%r y%r" % (ret, self.x, self.y))
        return ret

    def abs_to_01(self, loc) -> tuple[float, float]:
        """Given an absolute point in inches, returns a point in [0,1]^2 if in-bounds."""
        ret = ((loc[0]-self.x[0])/self.w, (loc[1]-self.y[0])/self.h)
        return ret

    def sub_bounds(self, x0, x1, y0, y1):
        ret = Bounds([self.x[0]+x0, self.x[0]+x1],
                     [self.y[0]+y0, self.y[0]+y1])
        if x0 < 0 or y0 < 0 or ret.x[1] > self.x[1] or ret.y[1] > self.y[1]:
            raise Exception("%r out of bounds %r" % (ret, self))
        return ret


def create_grid(b: Bounds, nx: int, ny: int, gutter: float) -> list[Bounds]:
    """Returns nx*ny bounds inset inside of b, separated by gutter in inches."""
    ret = []
    x, y = b.x[0], b.y[0]
    sx, sy = (b.w-gutter)/nx, (b.h-gutter)/ny
    for i in range(nx):
        for j in range(ny):
            ret.append(Bounds(
                (x + sx*i + gutter, x + sx*(i+1)),
                (y + sy*j + gutter, y + sy*(j+1))
            ))
    return ret


def default_init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_down = 40
    ad.options.pen_pos_up = 60
    ad.options.const_speed = True


def wait(ad: axidraw.AxiDraw, msg: str = "Press enter to continue..."):
    ad.penup()
    input(msg)


def safe_plot(draw_func: typing.Callable[[axidraw.AxiDraw], None], init_func=default_init, name=''):
    """Plots something on an AxiDraw, catching errors to return to a power-off state."""
    # Set up
    print("Connecting to plotter...")
    ad = axidraw.AxiDraw()
    ad.interactive()
    if name != '':
        ad.options.port = name
    init_func(ad)
    assert ad.connect()
    ad.penup()

    # Draw
    try:
        draw_func(ad)
        print("Going home...")
        ad.penup()
        ad.moveto(0, 0)
        disconnect_motors_off(ad)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
        ad.penup()
        sleep(0.1)
        ad.penup()
        disconnect_motors_off(ad)


def disconnect_motors_off(ad: axidraw.AxiDraw):
    print("Exiting, shutting off motors...")
    ad.disconnect()
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "disable_xy"
    ad.plot_run()


def safe_plot_seeds(draw_func: typing.Callable[[axidraw.AxiDraw], None], init_func=default_init):
    """Calls safe_plot multiple times, for a range of user-specified random seeds."""
    min_seed = int(input("Enter min seed: "))
    max_seed = int(input("Enter max seed: "))
    for seed in range(min_seed, max_seed + 1):
        print("")
        input("Ready for seed %d, hit enter to continue..." % seed)
        print("DRAWING SEED %d" % seed)
        random.seed(seed)
        np.random.seed(seed)
        safe_plot(draw_func, init_func)


def line_or_movep(ad: axidraw.AxiDraw, point: tuple[float, float]):
    if should_skip():
        return
    if ad.pen.status.pen_up:
        movep(ad, point)
        ad.pendown()
    else:
        linep(ad, point)


def movep(ad: axidraw.AxiDraw, point: tuple[float, float]):
    if should_skip():
        return
    ad.penup()  # work around a bug in the Axidraw library
    ad.moveto(point[0], point[1])


def linep(ad: axidraw.AxiDraw, point: tuple[float, float]):
    if should_skip():
        return
    ad.lineto(point[0], point[1])


moves_to_skip = 0


def should_skip():
    global moves_to_skip
    if moves_to_skip > 0:
        moves_to_skip -= 1
        return True
    return False


def skip(n: int):
    global moves_to_skip
    moves_to_skip = n
