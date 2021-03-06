#!/usr/bin/env python

import os
import logging

class Snapper:
  def set_resolution(self, width, height):
    self.width = width
    self.height = height

  def snap(self, file_path):
    self.call(self.snap_command(file_path))

  def snap_command(self, file_path):
    return "raspistill -w %s -h %s -o %s" % (self.width, self.height, file_path)

  def call(self, command):
    logging.info('System command call: %s' % command)
    os.system(command)
    logging.info('System command call done: %s' % command)
