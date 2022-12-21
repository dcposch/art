from pyaxidraw import axidraw
import argparse
import time


def read():
    ad = axidraw.AxiDraw()
    read_firmware_versions(ad)
    read_device_names(ad)
    print("To rename a plotter, plug in just that device, then run with <name>")


def rename(name: str):
    ad = axidraw.AxiDraw()
    print("BEFORE")
    names = read_device_names(ad)
    if len(names) != 1:
        raise Exception("expected 1 device, found %d" % len(names))

    rename_to(ad, name)
    time.sleep(1)

    print("AFTER")
    read_device_names(ad)


def rename_to(ad: axidraw.AxiDraw, name: str):
    print("Renaming to %r" % name)
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "write_name"+name
    ad.plot_run()


def read_firmware_versions(ad: axidraw.AxiDraw):
    print("Reading firmware version(s)...")
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "fw_version"
    ad.plot_run()


def read_device_names(ad: axidraw.AxiDraw):
    print("Reading device name(s)...")
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "list_names"
    ad.plot_run()
    return ad.name_list or []


if __name__ == "__main__":
    parser = argparse.ArgumentParser('configure')
    parser.add_argument('rename', type=str,
                        help='new device name', nargs='?', default='')
    args = parser.parse_args()

    if args.rename == '':
        read()
    else:
        rename(args.rename)
