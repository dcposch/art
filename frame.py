import common


def draw_frame(ad, bounds, dry_run=False):
    ad.penup()
    ad.moveto(bounds.x[0], bounds.y[0])
    if dry_run:
        ad.moveto(bounds.x[1], bounds.y[0])
        ad.moveto(bounds.x[1], bounds.y[1])
        ad.moveto(bounds.x[0], bounds.y[1])
        ad.moveto(bounds.x[0], bounds.y[0])
    else:
        ad.pendown()
        ad.lineto(bounds.x[1], bounds.y[0])
        ad.lineto(bounds.x[1], bounds.y[1])
        ad.lineto(bounds.x[0], bounds.y[1])
        ad.lineto(bounds.x[0], bounds.y[0])


def main(ad):
    w, h = 12, 8.9
    margin = 0.4
    draw_frame(ad, common.Bounds([margin, w-margin], [margin, h-margin]), True)


if __name__ == "__main__":
    common.safe_plot(main)
