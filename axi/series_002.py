
import math
import random
import typing

import numpy as np
from pyaxidraw import axidraw

import common
from vendor.perlin2d import generate_perlin_noise_2d


def init(ad: axidraw.AxiDraw):
    ad.options.pen_pos_up = 100
    ad.options.pen_pos_down = 35
    ad.options.speed_pendown = 35
    ad.options.const_speed = True
    print("Initialized: %r" % ad.options)


def draw(ad: axidraw.AxiDraw):
    w, h, m = 9, 9, 0.5  # canvas dimensions and margin, in inches
    b = common.Bounds([m, w-m], [m, h-m])
    paint_loc_1 = (0, 0)  # (10.8, 0.7)  # right tub
    paint_loc_2 = (0, 0)  # (10.8, 2.5)  # middle tub

    # Perlin noise flow field
    w = 256
    n_density = generate_perlin_noise_2d((w, w), (8, 8))
    n_dir = generate_perlin_noise_2d((w, w), (8, 8))

    # TODO: invert
    n_density = -1.0 * n_density

    # Strokes
    strokes = gen_strokes(b, n_density, n_dir, 500, 40)
    strokes_1 = shorten_strokes(strokes, b)
    ad.penup()
    ad.moveto(paint_loc_1[0], paint_loc_1[1])
    input("Painting layer 1, press enter to continue...")
    draw_strokes(ad, paint_loc_1, strokes_1)

    strokes_2 = micro_strokes(strokes)
    ad.penup()
    ad.moveto(paint_loc_2[0], paint_loc_2[1])
    input("Painting layer 2, press enter to continue...")
    draw_strokes(ad, paint_loc_2, strokes_2)

    return

    strokes_3 = list(
        map(lambda s: s[:5],
            filter(lambda s: random.random() < dot_prob(s[0], b, n_density),
                   strokes_2)))
    ad.penup()
    ad.moveto(paint_loc_2[0], paint_loc_2[1])
    input("Dotting layer 2, press enter to continue...")
    draw_strokes(ad, paint_loc_2, strokes_3)


def dot_prob(s0: tuple[float, float], b: common.Bounds, n_density: np.ndarray) -> float:
    w = n_density.shape[0]
    p0 = b.abs_to_01(s0)
    thin = n_density[int(min(0.9999, p0[0])*w),
                     int(min(0.9999, p0[1])*w)] + 0.2
    thic = (1 - thin)/1.2
    assert thic >= 0

    return thic**2


def shorten_strokes(strokes: list[list[tuple[float, float]]], b: common.Bounds):
    return list(map(lambda stroke: shorten_stroke(stroke, b.x[0], b.w), strokes))


def shorten_stroke(stroke: list[tuple[float, float]], x_min: float, w: float) -> list[tuple[float, float]]:
    # Randomly shorten early strokes
    x_frac = (stroke[0][0] - x_min)/w  # 0 = earliest, 1 = latest
    x_frac = (0.2 + x_frac)/1.2  # 0.2 = earliest, 1 = latest
    new_len = int(len(stroke) * (x_frac + random.random()*(1-x_frac)))
    return stroke[: new_len]


def micro_strokes(strokes: list[list[tuple[float, float]]]):
    return list(map(micro_stroke, strokes))


def micro_stroke(stroke: list[tuple[float, float]]):
    offset = (
        random.normalvariate(0, 0.1),
        random.normalvariate(0.1, 0.1)
    )
    short = stroke[:int(5 + 10*random.random())]
    return list(map(lambda p: (p[0]+offset[0], p[1]+offset[1]), short))


def draw_strokes(ad: axidraw.AxiDraw, paint_loc: tuple[float, float], strokes: typing.Iterable[list[tuple[float, float]]]):
    px, py = paint_loc
    def prand(): return (random.random() - 0.5)*0.8

    strokes.sort(key=lambda s: s[0][1])  # sort by y axis
    prev_start = (100, 0)
    for i, stroke in enumerate(strokes):
        start = stroke[0]
        if start[0] < prev_start[0] and px != 0:
            # Dip the paint brush
            ad.moveto(px+prand(), py+prand())
            ad.pendown()
            ad.penup()
        prev_start = start

        # Draw the next stroke
        for i, point in enumerate(stroke):
            sx, sy = point
            if i == 0:
                ad.moveto(sx, sy)
                ad.pendown()
            else:
                ad.lineto(sx, sy)
        ad.penup()

    print("Done")


def gen_strokes(b: common.Bounds, n_density: np.ndarray, n_dir: np.ndarray, num_strokes=100, stroke_len=60) -> typing.Iterable[list[tuple[float, float]]]:
    ret: list[list[tuple[float, float]]] = []
    w = n_density.shape[0]
    while len(ret) < num_strokes:
        x, y = np.random.random(), np.random.random()
        dense = n_density[int(x*w), int(y*w)]
        if np.random.random() - 0.2 < dense:
            continue
        stroke = [(x, y)]
        r = 1/w
        for _ in range(stroke_len):
            dir = n_dir[int(x*w), int(y*w)]
            x += math.cos(dir) * r
            y += math.sin(dir) * r
            if x < 0 or x >= 1 or y < 0 or y >= 1:
                break
            stroke.append((x, y))
        if len(stroke) < stroke_len:
            continue

        stroke_in = list(map(lambda p: b.loc(b.w*p[0], b.h*p[1]), stroke))
        ret.append(stroke_in)

    return ret


def main():
    common.safe_plot_seeds(draw, init)


if __name__ == "__main__":
    main()
