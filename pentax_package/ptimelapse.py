"""Pentax Timelapse.

Usage:
  ptimelapse [-f <prefix>] [-t <shutter-speed> ] [-a <aperture> ] [-i <iso> ] [-d <directory>] [-m <mode>] [-l <lapse>]
             [-c <count>] [-s] [-b <bucket>] [-k <s3_key>]
  ptimelapse (-h | --help)

Options:
  -h --help              Show this screen.
  -f <prefix>            Output File Prefix [default: ptimelapse]
  -t <shutter-speed>     Shutter Speed, auto if not specified
  -a <aperature>         Aperture, auto if not specified
  -i <iso>               ISO, auto if not specified
  -d <directory>         Output Directory [default: .]
  -m <mode>              Camera mode [default: GREEN]
  -l <lapse>             Lapse Duration in seconds [default: 30], needs to be 5 seconds or greater
  -c <count>             Number of frames to take if not specified run forever [default: 5]
  -s                     Upload to S3
  -b <bucket>            S3 bucket [default: pentax-timelapse]
  -k <s3_key>            S3 Key to put files inside bucket [default: default]
"""

from docopt import docopt
from pentax_package import camera_control, s3_upload
import os
import time
import sys
import logging


logger = logging.getLogger('ptimelapse')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    arguments = docopt(__doc__, argv=args)

    i = 1

    camera = camera_control.Camera()

    if arguments['-m'] != 'GREEN':
        camera.exposure_mode = arguments['-m']
        if arguments['-t']:
            camera.shutter_speed = arguments['-t']
        if arguments['-a']:
            camera.aperture = arguments['-a']
        if arguments['-i']:
            camera.iso = arguments['-i']

    if not os.path.exists(arguments['-d']):
        logger.error("Destination folder does not exist")
        exit(1)

    if int(arguments['-l']) < 5:
        logger.error("Minimum lapse duration is 5 seconds")
        exit(1)

    uploader = None
    if arguments['-s']:
        uploader = s3_upload.S3Uploader(arguments['-d'])
        uploader.bucket = arguments['-b']
        uploader.key_path = arguments['-k']
        uploader.run()

    while True:
        if i > int(arguments['-c']):
            logger.info("Finished")
            break
        filename = os.path.join(arguments['-d'], str(i).zfill(8) + '-' + arguments['-f'] + '.jpg')
        logger.info("Taking Picture")
        time_taken = time.time()
        camera.take_picture(filename)
        time_took = time.time() - time_taken
        sleep_time = int(arguments['-l']) - time_took
        if sleep_time > 0:
            logger.info("Sleeping %f seconds" % sleep_time)
            time.sleep(sleep_time)
        i += 1

    if arguments['-s']:
        uploader.stop = True
        uploader.join()

    exit(0)

if __name__ == "__main__":
    main()
