import json


def main(event, context):
    body = {
        "message": "hello"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response