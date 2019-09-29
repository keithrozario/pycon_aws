import json


def main(event, context):
    body = {
        "message": "Goodbye from Python"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response