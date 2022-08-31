import math
import common

# Bounds for letter paper, in inches
margin = [0.5, 0.5]
bx = [margin[0], 12-margin[0]]
by = [margin[1], 9-margin[1]]

print("Plotting an oval spiral")
# Center
cx = sum(bx) / 2
cy = sum(by) / 2

# Plot params
r_offset = 0.325
step_rad = 0.01
in_per_rev = 0.4
wobble_max_in = 0.15
wobbles_per_in = 3
num_revs = 18


def draw_spiral(ad):
    for i in range(math.floor(num_revs * 2 * math.pi / step_rad)):
        # Main spiral
        theta = i * step_rad
        r = r_offset + theta / (2 * math.pi) * in_per_rev
        x = cx + math.cos(theta) * r
        y = cy + math.sin(theta) * r

        # Add wobble for texture
        wobbliness = wobble_func(x, y)
        wobble_rho = i * step_rad * r * wobbles_per_in * 2 * math.pi
        wobble = math.sin(wobble_rho) * wobbliness * wobble_max_in
        x += math.cos(theta) * wobble
        y += math.sin(theta) * wobble

        common.lineto_or_moveto(ad, x, y)


def wobble_func(x, y):
    """Given x and y in inches, returns a value between 0 (no wobble) and 1"""
    # 2D sine wave
    # return (0.5 + (math.sin(x * 3) * math.sin(y * 3)) / 2)**2

    # Curved waves
    return ((math.sin(y * 2 + y**2 / 20 + x**2 / 60) + 1) / 2)**2


if __name__ == "__main__":
    common.safe_plot(draw_spiral)
