from pyaxidraw import axidraw
import math
import random
import collections

def safe_plot(draw_func):
    # Set up
    print("Connecting to plotter...")
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.options.pen_pos_down = 10
    ad.options.pen_pos_up = 50
    ad.options.const_speed = True
    ad.connect()

    # Draw
    try:
        draw_func(ad)
    except Exception as e:
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