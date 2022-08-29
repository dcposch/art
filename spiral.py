from pyaxidraw import axidraw
import math
import random
import collections

ad = axidraw.AxiDraw()
ad.interactive()
ad.options.pen_pos_down = 10
ad.options.pen_pos_up = 60
ad.options.const_speed = True
ad.connect()

# Bounds for letter paper, in inches
margin = [0.5, 0.5]
bx = [margin[0], 12-margin[0]]
by = [margin[1], 9-margin[1]]

print("Plotting an oval spiral")
# Center
cx = sum(bx) / 2
cy = sum(by) / 2

ad.penup()

# Plot
step_rad = 0.01
in_per_rev = 0.25
wobble_max_in = 0.12
num_revs = 16
for i in range(math.floor(num_revs * 2 * math.pi / step_rad)):
    # Main spiral
    theta = i * step_rad
    r = 0.1 + theta / (2 * math.pi) * in_per_rev
    x = cx + math.cos(theta) * r
    y = cy + math.sin(theta) * r

    # Add wobble
    wobbliness = 1 + (math.sin(x * 3) * math.sin(y * 3)) / 2
    wobble_rho = i * step_rad * r * 20
    wobble = math.sin(wobble_rho) * wobbliness * wobble_max_in
    x += math.cos(theta) * wobble
    y += math.sin(theta) * wobble   

    if ad.pen.status.pen_up:
        ad.moveto(x, y)
        ad.pendown()
    else:
        ad.lineto(x, y)

# Move home
ad.penup()
ad.moveto(0, 0)

# Done
ad.disconnect()
