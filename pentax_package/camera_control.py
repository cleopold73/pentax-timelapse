import subprocess
import os
import logging

logger = logging.getLogger('ptimelapse')

class Camera:
    exposure_mode = "GREEN"
    iso = None
    aperture = None
    shutter_speed = None
    resolution = '10'
    quality = '3'
    output_file = "out.jpg"
    temp_file = "/tmp/temp.jpg"
    pslr_shoot_timeout = 10
    FNULL = open(os.devnull, 'w')

    def take_picture(self, output_file=None):
        if output_file:
            self.output_file = output_file
        args = ['pslr-shoot', '-m', self.exposure_mode, '-r', self.resolution, '-q', self.quality,
                '-o', self.temp_file]

        if self.iso:
            args.append('-i')
            args.append(self.iso)

        if self.aperture:
            args.append('-a')
            args.append(self.aperture)

        if self.shutter_speed:
            args.append('-t')
            args.append(self.shutter_speed)

        try:
            subprocess.run(args, check=True, timeout=self.pslr_shoot_timeout, stdout=self.FNULL)
        except(subprocess.CalledProcessError):
            logger.error("Failed to take picture non zero error code from pslr-shoot")
            raise
        except(subprocess.TimeoutExpired):
            logger.error("Failed to take picture call to pslr-shoot timed out")
            raise
        os.rename(self.temp_file, self.output_file)
