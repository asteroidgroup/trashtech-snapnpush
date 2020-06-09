import os
import threading
import time
import logging
import time
import datetime

from snap import Snapper
from s3_client import S3Client
from trashtech_api import TrashtechApi
from gsm_controller import GsmController

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class TrashtechApp:
  def __init__(self):
    self.trashtech_client = TrashtechApi()
    self.s3_client = S3Client()
    self.snapper = Snapper()
    self.snapper.set_resolution(640, 480)
    self.gsm_controller = GsmController()

  def reload_configuration(self):
    self.configuration = self.trashtech_client.configuration()

  def interval(self):
    self.configuration['interval']

  def call_snap(self, filename):
    self.snapper.snap(filename)

  def init_gsm(self):
    self.gsm_controller.enable()

  def run(self):
    if self.gsm_controller.is_ppp_interface_present() is not True:
      self.init_gsm()
      time.sleep(50)

    configuration = self.trashtech_client.configuration()

    image_created_at_timestamp = time.time()
    complete_file_path = 'TT_%s.jpg' % image_created_at_timestamp

    self.call_snap(complete_file_path)
    time.sleep(5)

    response = self.s3_client.upload(complete_file_path)

    device_reference = '000006'
    image_created_at = datetime.datetime.fromtimestamp(image_created_at_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    self.trashtech_client.create_status(device_reference, response.e_tag, complete_file_path, image_created_at)

    self.gsm_controller.disable()

    thread = threading.Timer(configuration['photo_interval']-50, trashtech_app.run)
    thread.start()

if __name__ == '__main__':
  trashtech_app = TrashtechApp()
  trashtech_app.run()
