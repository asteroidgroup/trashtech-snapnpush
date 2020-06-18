#!/usr/bin/env python

import requests
import logging
import json
import base64

class TrashtechApi:
  api_base = 'http://trashtech.herokuapp.com/api'

  def GetConfiguration(self):
    url = "%s/device_configurations/1" % self.api_base
    logging.info('[INFO] request call: %s' % url)

    response = requests.get(url)
    json = response.json()
    logging.info('[INFO] json response: %s' % json)

    return json

  def create_status(self, device_reference, complete_file_path, image_created_at):
    with open(complete_file_path, "rb") as image_file:
      encoded_image = base64.b64encode(image_file.read())

    request_json = {
      "device_status": {
        "image_created_at": image_created_at,
        "image_base": "data:image/jpg;base64,%s" % encoded_image,
        "device_reference": device_reference,
        "container_identifier_number": device_reference,
      }
    }

    # logging.info("[INFO] request json: %s", request_json)
    url = "%s/device_statuses/" % (self.api_base)
    logging.info("[INFO] request call: %s", url)

    response = requests.post(url, json = request_json)
    json = response.json()
    logging.info('[INFO] json response: %s' % json)

    return json
