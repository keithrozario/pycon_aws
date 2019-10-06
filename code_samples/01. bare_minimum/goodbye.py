import json


def main(event, context):
    body = {
        "message": "Goodbye from Pycon"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response