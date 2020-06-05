import os
import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

AWS_ACCESS_KEY_ID = "AKIAJGG5DJ3XAM2NESYQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_BUCKET_NAME = "trashtech-images-1"

class S3Client:
  def __init__(self):
    self.session = boto3.Session(
      aws_access_key_id=AWS_ACCESS_KEY_ID,
      aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

  def upload(self, complete_file_path):
    if complete_file_path is None:
      raise ValueError("Please enter a valid and complete file path")

    s3 = self.session.resource('s3')
    data = open(os.path.normpath(complete_file_path), 'rb')
    file_basename = os.path.basename(complete_file_path)

    try:
      res = s3.Bucket(AWS_BUCKET_NAME).put_object(Key=file_basename, Body=data)
      logging.info('[INFO] Image sent')
      logging.info('[INFO] e_tag= %s' % (res.e_tag))
      logging.info('[INFO] metadata= %s' % (res.metadata))

    except ClientError as e:
      logging.error(e)
      return False

    return res
