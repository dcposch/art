import common


def draw_frame(ad, bounds):
    ad.penup()
    ad.moveto(bounds.x[0], bounds.y[0])
    ad.pendown()
    ad.lineto(bounds.x[1], bounds.y[0])
    ad.lineto(bounds.x[1], bounds.y[1])
    ad.lineto(bounds.x[0], bounds.y[1])
    ad.lineto(bounds.x[0], bounds.y[0])


def main(ad):
    margin = 0.5
    draw_frame(ad, common.Bounds([margin, 12-margin], [margin, 9-margin]))


if __name__ == "__main__":
    common.safe_plot(main)
