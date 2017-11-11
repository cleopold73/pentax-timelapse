import boto3
import threading
import os
import time
import logging

logger = logging.getLogger('ptimelapse')

class S3Uploader:

    key_path = 'default'
    bucket = 'pentax-timelapse'
    s3 = boto3.resource('s3')
    monitor_interval = 30
    delete_after_upload = True
    stop = False

    def __init__(self, monitor_directory):
        self.monitor_thread = threading.Thread(target=self.monitor)
        self.monitor_directory = monitor_directory

    def upload(self, filename):
        key = self.key_path + '/' + filename
        local_path = os.path.join(self.monitor_directory, filename)
        try:
            data = open(local_path, 'rb')
        except Exception as e:
            logger.exception("failed to open probably second time it was tried")
        else:
            logger.info("Uploading %s" % local_path)
            try:
                self.s3.Bucket(self.bucket).put_object(Key=key, Body=data)
            except Exception as e:
                logger.exception("Upload failed will try again next time")
                data.close()
            else:
                data.close()
                if self.delete_after_upload:
                    try:
                        os.unlink(local_path)
                    except Exception as e:
                        logger.exception("failed to delete probably second time it was tried")

    def monitor(self):
        logger.info("Starting to monitor files for upload")
        while True:
            file_list = os.listdir(self.monitor_directory)
            for file in file_list:
                self.upload(file)
            if self.stop:
                break
            time.sleep(self.monitor_interval)
        logger.info("Exiting S3 upload thread")

    def run(self):
        self.monitor_thread.start()

    def join(self):
        self.monitor_thread.join()
