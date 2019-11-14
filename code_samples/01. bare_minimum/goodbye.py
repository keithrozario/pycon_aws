import json


def main(event, context):
    body = {
        "message": "May the force be with you!!!!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
