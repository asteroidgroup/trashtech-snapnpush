import os
import logging
import ifcfg

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class GsmController:
  def enable(self):
    self.on()
    self.on_ppp()

  def disable(self):
    self.off()
    self.off_ppp()

  def on_ppp(self):
    self.call('sudo pon u-GSM')

  def off_ppp(self):
    self.call('sudo poff u-GSM')

  def on(self):
    self.call('sudo sh /home/pi/u-GSM-ppp/poweronGSM')

  def off(self):
    self.call('sudo sh /home/pi/u-GSM-ppp/poweroffGSM')

  def call(self, command):
    logging.info('[INFO] System command call: %s' % command)
    os.system(command)
    logging.info('[INFO] System command call done: %s' % command)

  def is_ppp_interface_present(self):
    exists = False

    for name, interface in ifcfg.interfaces().items():
      if interface['device'] == 'ppp0':
        exists = True

    if exists:
      logging.info('[INFO] ppp0 interface is present.')
    else:
      logging.info('[INFO] ppp0 interface is not present.')

    return exists
