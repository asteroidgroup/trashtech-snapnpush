import os
import threading
import time
import logging

from snap import Snapper
from s3_client import S3Client
from trashtech_api import TrashtechApi

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class TrashtechApp:
  def __init__(self):
    self.trashtech_client = TrashtechApi()
    self.configuration = self.trashtech_client.configuration()
    self.snapper = Snapper()

  def reload_configuration(self):
    self.configuration = self.trashtech_client.configuration()

  def interval(self):
    self.configuration()['interval']

  def call_snap(self):
    file_path = "TT_%s.jpg" % ('test')
    self.snapper.snap(file_path)

  def take_action(self):
    self.call_snap()

if __name__ == '__main__':
  trashtech_app = TrashtechApp()
  trashtech_app.call_snap()
