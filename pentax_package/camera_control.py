import subprocess


class Camera:
    exposure_mode = "GREEN"
    iso = None
    aperture = None
    shutter_speed = None
    resolution = '10'
    quality = '3'
    output_file = "out.jpg"

    def take_picture(self, output_file=None):
        if output_file:
            self.output_file = output_file
        args = ['pslr-shoot', '-m', self.exposure_mode, '-r', self.resolution, '-q', self.quality,
                '-o', self.output_file]

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
            subprocess.run(args, check=True)
        except(subprocess.CalledProcessError):
            print("Failed to take picture non zero error code from pslr-shoot")
            raise
