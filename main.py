import os
import threading
import time
import logging

from snap import Snapper
from s3_client import S3Client
from trashtech_api import TrashtechApi
from gsm_controller import GsmController

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class TrashtechApp:
  def __init__(self):
    self.trashtech_client = TrashtechApi()
    self.configuration = self.trashtech_client.configuration()
    self.snapper = Snapper()
    self.gsm_controller = GsmController()

  def reload_configuration(self):
    self.configuration = self.trashtech_client.configuration()

  def interval(self):
    self.configuration()['interval']

  def call_snap(self):
    file_path = "TT_%s.jpg" % ('test')
    self.snapper.snap(file_path)

  def init_gsm(self):
    self.gsm_controller.enable()

if __name__ == '__main__':
  trashtech_app = TrashtechApp()
  trashtech_app.init_gsm()
  time.sleep(10000)
  trashtech_app.call_snap()
