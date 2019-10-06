import os
import json
import tempfile

import boto3
from aws_xray_sdk.core import xray_recorder


def main(event, context):

    # Code block to download config file into config dict
    s3 = boto3.resource('s3')
    source_bucket = s3.Bucket(os.environ['SOURCE_BUCKET'])
    config_file = 'config.json'

    with tempfile.SpooledTemporaryFile() as data:
        source_bucket.download_fileobj(config_file, data)
        data.seek(0)
        config = json.loads(data.read())

    return json.dumps(config)