"""Pentax Timelapse.

Usage:
  ptimelapse [-f <prefix>] [-t <shutter-speed> ] [-a <aperture> ] [-i <iso> ] [-d <directory>] [-m <mode>] [-l <lapse>]
             [-c <count>]
  ptimelapse (-h | --help)

Options:
  -h --help              Show this screen.
  -f <prefix>            Output File Prefix [default: ptimelapse]
  -t <shutter-speed>     Shutter Speed, auto if not specified
  -a <aperature>         Aperture, auto if not specified
  -i <iso>               ISO, auto if not specified
  -d <directory>         Output Directory [default: .]
  -m <mode>              Camera mode [default: GREEN]
  -l <lapse>             Lapse Duration in seconds [default: 30]
  -c <count>             Number of frames to take if not specified run forever [default: 5]
"""
from docopt import docopt
from pentax_package import camera_control
import os
import time

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)

    i = 1

    camera = camera_control.Camera()

    if not os.path.exists(arguments['-d']):
        print("Destination folder does not exist")
        exit(1)

    while True:
        if i > int(arguments['-c']):
            print("Finished")
            exit(0)
        filename = os.path.join(arguments['-d'], str(i).zfill(8) + '-' + arguments['-f'] + '.jpg')
        print("Taking Picture")
        camera.take_picture(filename)
        time.sleep(int(arguments['-l']))
        i += 1
