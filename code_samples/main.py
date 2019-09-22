import boto3
import os
import tempfile
import time
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')


def main(event, context):

    key = event.get('key', '10.txt')
    iter = event.get('iter', 10)
    source_bucket = s3.Bucket(os.environ['SOURCE_BUCKET'])
    dest_bucket = s3.Bucket(os.environ['DEST_BUCKET'])

    using = event.get('using', 'memory')

    response = copy(key=key,
                    iter=iter,
                    source_bucket=source_bucket,
                    dest_bucket=dest_bucket,
                    using=using)

    return response


def copy(key, iter, source_bucket, dest_bucket, using):

    """
    key: Key of S3 object to be downloaded and uploaded
    iter: Number of times to upload/download the key
    source_bucket: Source bucket to copy from
    dest_bucket: Dest bucket to copy to
    using: using 'memory' or 'disk'
    """

    if using == 'memory':
        copy_function = in_memory_copy
    else:
        copy_function = on_disk_copy

    init_length = source_bucket.Object(key).content_length
    logger.info(f"Starting file size: {init_length:,}")

    start = time.time()
    for _ in range(iter):
        copy_function(source_bucket, dest_bucket, key)
    end = time.time()

    final_length = dest_bucket.Object(key).content_length
    logger.info(f"Ending file size: {final_length:,}")

    return json.dumps({'key': key,
                       'iter': iter,
                       'elapsed_time': (end-start)})


def on_disk_copy(source_bucket, dest_bucket, key):

    """
    This function downlaods file to disk, and uploads file from disk
    """
    logger.info("Using On Disk copy...")

    logger.info(f"Downloading {key} from {source_bucket}")
    source_bucket.download_file(key, f'/tmp/{key}')

    logger.info(f"Uploading {key} to {dest_bucket}")
    dest_bucket.upload_file(f'/tmp/{key}', key)
    logger.info(f"Uploaded {key} to destination")

    return None


def in_memory_copy(source_bucket, dest_bucket, key):

    """
    This function downloads file in memory, and uploads file from memory
    """

    # with io.BytesIO() as byte_stream:
    #     logger.info("Beggining In-Memory Download")
    #     source_bucket.download_fileobj(key, byte_stream)
    #     logger.info("Resetting to Zero")
    #     byte_stream.seek(0)  # reset stream to beginning of file
    #     logger.info("Uploading to S3")
    #     dest_bucket.upload_fileobj(byte_stream, key)
    #     logger.info(f"Uploaded {key} with size {byte_stream.__sizeof__()}")

    logger.info("Using In Memory copy...")

    with tempfile.SpooledTemporaryFile() as data:
        logger.info(f"Downloading {key} from {source_bucket}")
        source_bucket.download_fileobj(key, data)
        data.seek(0)
        logger.info(f"Uploading {key} to {dest_bucket}")
        dest_bucket.upload_fileobj(data, key)

    return None


if __name__ == '__main__':

    bucket_name = 'terraform-20190921073940359200000001'
    source_bucket = s3.Bucket(bucket_name)
    dest_bucket = s3.Bucket(bucket_name)

    copy(key='10.txt',
         iter=10,
         source_bucket=source_bucket,
         dest_bucket=dest_bucket,
         using='memory')
