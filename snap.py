#!/usr/bin/env python

import os

class Snapper:
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def snap(self, file_path):
    os.system(snap_command(self, file_path))

  def snap_command(self, file_path):
    "raspistill -w %s -h %s -o %s" % (self.width, self.height, file_path)
