import os
import boto3

AWS_ACCESS_KEY_ID = "AKIAJGG5DJ3XAM2NESYQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_BUCKET_NAME = "trashtech-images-1"

session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_file_to_s3(complete_file_path):
  if complete_file_path is None:
    raise ValueError("Please enter a valid and complete file path")

  session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
  )
  s3 = session.resource('s3')
  data = open(os.path.normpath(complete_file_path), 'rb')
  file_basename = os.path.basename(complete_file_path)
  s3.Bucket(AWS_BUCKET_NAME).put_object(Key=file_basename, Body=data)

if __name__ == '__main__':
  upload_file_to_s3('tmp/supercat.png')
