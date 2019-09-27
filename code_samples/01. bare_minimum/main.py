import json


def main(event, context):
    body = {
        "message": "Go Python"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response