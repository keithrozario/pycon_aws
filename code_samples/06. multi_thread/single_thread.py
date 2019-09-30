import logging
from datetime import datetime
import boto3
import time

logger = logging.getLogger()
level = logging.INFO

ssm_client = boto3.client('ssm')
table_name = ssm_client.get_parameter(Name='/pycon/dynamodb_table_name')['Parameter']['Value']


def main(event, context):

    num_items = event.get('num_items', 100)
    result = start(num_items)

    return result


def start(num_items):

    items = gen_items(num_items)
    response = write_items(items)

    return response


def gen_items(num_items):

    pk = datetime.now().isoformat()
    ttl_value = int(time.time() + 8*3600)

    results = []

    for i in range(num_items):
        results.append({'pk': {'S': pk},
                        'rk': {'N': str(i)},
                        'expires_in': {'N': str(ttl_value)}})
    return results


def write_items(items):

    """
    Receives a list of text to be processed, one element per row
    Returns a list of dictionaries to be combined into a single file
    """
    dynamodb_client = boto3.client('dynamodb')
    responses = []

    for item in items:
        response = dynamodb_client.put_item(TableName=table_name,
                                            Item=item)
        responses.append(response)

    return responses


if __name__ == '__main__':

    start(100)
