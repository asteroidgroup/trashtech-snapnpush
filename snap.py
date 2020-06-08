#!/usr/bin/env python

import os
import logging

class Snapper:
  def set_resolution(self, width, height):
    self.width = width or 640
    self.height = height or 480

  def snap(self, file_path):
    self.call(self.snap_command(file_path))

  def snap_command(self, file_path):
    "raspistill -w %s -h %s -o %s" % (self.width, self.height, file_path)

  def call(self, command):
    logging.info('[INFO] System command call: %s' % command)
    os.system(command)
    logging.info('[INFO] System command call done: %s' % command)
