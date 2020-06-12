import os
import threading
import time
import datetime
import logging

from snap import Snapper
from s3_client import S3Client
from trashtech_api import TrashtechApi
from gsm_controller import GsmController

logging.basicConfig(format='[INFO] %(asctime)s - %(message)s', level=logging.INFO)

DEVICE_REFERENCE = '000006'
GSM_WARMUP_TIME = 50 # 50 seconds
WIDTH = 640
HEIGHT = 480
FILE_FORMAT = "TT_%s.jpg"
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

class TrashtechApp:
  def initialize(self):
    self.trashtech_client = TrashtechApi()
    self.s3_client = S3Client()
    self.snapper = Snapper()
    self.snapper.set_resolution(WIDTH, HEIGHT)
    self.gsm_controller = GsmController()

  def retrive_configuration(self):
    self.configuration = self.trashtech_client.configuration()

  def interval(self):
    self.configuration['photo_interval']

  def call_snap(self, filename):
    self.snapper.snap(filename)

  def init_gsm(self):
    if self.gsm_controller.is_ppp_interface_present() is not True:
      self.init_gsm()
      time.sleep(GSM_WARMUP_TIME)

  def run(self):
    self.init_gsm()

    image_created_at_timestamp = time.time()
    complete_file_path = FILE_FORMAT % image_created_at_timestamp

    self.call_snap(complete_file_path)
    time.sleep(1)

    response = self.s3_client.upload(complete_file_path)

    image_created_at = datetime.datetime.fromtimestamp(image_created_at_timestamp).strftime(TIMESTAMP_FORMAT)
    self.trashtech_client.create_status(DEVICE_REFERENCE, response.e_tag, complete_file_path, image_created_at)

    self.gsm_controller.disable()

    thread = threading.Timer(self.interval() - GSM_WARMUP_TIME, trashtech_app.run)
    thread.start()

if __name__ == '__main__':
  logging.info("Hi. We are TRASHTECH. Let's play.")

  trashtech_app = TrashtechApp()
  trashtech_app.retrive_configuration()
  trashtech_app.initialize()
  trashtech_app.run()
