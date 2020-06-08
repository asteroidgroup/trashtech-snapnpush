#!/usr/bin/env python

import requests
import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class TrashtechApi:
  api_base = 'http://trashtech.herokuapp.com/api'

  def configuration(self):
    url = "%s/device_configurations/1" % self.api_base
    logging.info('[INFO] request call: %s' % url)

    response = requests.get(url)
    json = response.json()
    logging.info('[INFO] json response: %s' % json)

    return json

  def create_status(self, device_reference, e_tag):
    request_json = {
      "device_status": {
        "image_name": e_tag,
        "image_created_at": "",
        "image_e_tag": e_tag,
        "image_size": "",
        "device_reference": device_reference,
        "container_identifier_number": device_reference,
      }
    }
    logging.info("[INFO] request json: %s", request_json)
    url = "%s/device_statuses/%s" % (self.api_base, device_reference)
    logging.info("[INFO] request call: %s", url)

    response = requests.post(url, json = request_json)
    json = response.json()
    logging.info('[INFO] json response: %s' % json)

    return json
