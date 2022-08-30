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
r_offset = 0.125
step_rad = 0.01
in_per_rev = 0.25
wobble_max_in = 0.15
wobbles_per_in = 4
num_revs = 8


def draw_spiral(ad):
    for i in range(math.floor(num_revs * 2 * math.pi / step_rad)):
        # Main spiral
        theta = i * step_rad
        r = r_offset + theta / (2 * math.pi) * in_per_rev
        x = cx + math.cos(theta) * r
        y = cy + math.sin(theta) * r

        # Add wobble for texture
        wobbliness = (0.5 + (math.sin(x * 3) * math.sin(y * 3)) / 2)**2
        wobble_rho = i * step_rad * r * wobbles_per_in * 2 * math.pi
        wobble = math.sin(wobble_rho) * wobbliness * wobble_max_in
        x += math.cos(theta) * wobble
        y += math.sin(theta) * wobble

        common.lineto_or_moveto(ad, x, y)


common.safe_plot(draw_spiral)
