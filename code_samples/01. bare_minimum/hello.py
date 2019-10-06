import json


def main(event, context):
    body = {
        "message": "Majulah Singapore"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response