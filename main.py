import os
import threading
import time
import datetime
import logging

from snap import Snapper
from trashtech_api import TrashtechApi
from gsm_controller import GsmController

DEVICE_REFERENCE = '000006'
FILE_FORMAT = "%s/TT_%s.jpg"
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

class TrashtechApp:
  def initialize(self):
    self.trashtech_client = TrashtechApi()
    self.snapper = Snapper()
    self.gsm_controller = GsmController()

  def retrive_configuration(self):
    self.configuration = self.trashtech_client.configuration()
    self.snapper.set_resolution(self.configuration['photo_width'], self.configuration['photo_height'])

  def interval(self):
    return self.configuration['photo_interval']

  def call_snap(self, filename):
    self.snapper.snap(filename)

  def init_gsm(self):
    if self.gsm_controller.is_ppp_interface_present() is not True:
      self.gsm_controller.enable()

  def wait_for_gsm(self):
    while self.gsm_controller.is_ppp_interface_present() is not True:
      logging.info("[INFO] Waiting for GSM..")
      time.sleep(2)

    if self.gsm_controller.is_ppp_interface_present():
      logging.info("[INFO] GSM module enabled")

    time.sleep(5)

  def run(self):
    start_time = time.time()

    self.init_gsm()

    image_created_at_timestamp = time.time()
    complete_file_path = FILE_FORMAT % ('/home/pi/trashtech-snapnpush/images', image_created_at_timestamp)

    self.call_snap(complete_file_path)
    self.wait_for_gsm()

    image_created_at = datetime.datetime.fromtimestamp(image_created_at_timestamp).strftime(TIMESTAMP_FORMAT)
    self.trashtech_client.create_status(DEVICE_REFERENCE, complete_file_path, image_created_at)

    self.gsm_controller.disable()
    logging.info("[INFO] GSM module disabled")

    execution_time = time.time() - start_time
    logging.info("[INFO] Execution time: %s" % execution_time)

    wait_iterval_time = int(float(self.interval()) - execution_time)
    logging.info("[INFO] Wait interval time: %s" % wait_iterval_time)

    thread = threading.Timer(wait_iterval_time, trashtech_app.run)
    thread.start()

if __name__ == '__main__':
  logging.basicConfig(
    format='[INFO] %(asctime)s - %(message)s',
    level=logging.INFO
  )

  logging.info("Hi. We are TRASHTECH. Let's play.")

  trashtech_app = TrashtechApp()
  trashtech_app.initialize()
  trashtech_app.init_gsm()
  trashtech_app.wait_for_gsm()
  trashtech_app.retrive_configuration()
  trashtech_app.run()
