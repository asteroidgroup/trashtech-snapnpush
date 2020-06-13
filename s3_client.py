import os
import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='[INFO] %(asctime)s - %(message)s', level=logging.INFO)

class S3Client:
  def set_credentials(self, aws_access_key, aws_secret_access_key, aws_bucket_name):
    self.aws_access_key = aws_access_key
    self.aws_secret_access_key = aws_secret_access_key
    self.aws_bucket_name = aws_bucket_name
    self.session = boto3.Session(
      aws_access_key_id = self.aws_access_key,
      aws_secret_access_key = self.aws_secret_access_key
    )

  def upload(self, complete_file_path):
    if complete_file_path is None:
      raise ValueError("Please enter a valid and complete file path")

    s3 = self.session.resource('s3')
    data = open(os.path.normpath(complete_file_path), 'rb')
    file_basename = os.path.basename(complete_file_path)

    try:
      res = s3.Bucket(self.aws_bucket_name).put_object(Key=file_basename, Body=data)
      logging.info('Image sent')
      logging.info('e_tag= %s' % (res.e_tag))
      logging.info('metadata= %s' % (res.metadata))

    except ClientError as e:
      logging.error(e)
      return False

    return res
