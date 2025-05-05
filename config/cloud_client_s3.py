import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()


cloud_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
    endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
    config=Config(signature_version='s3')
)


