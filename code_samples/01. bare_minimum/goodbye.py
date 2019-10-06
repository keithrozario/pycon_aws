import json


def main(event, context):
    body = {
        "message": "Woooaaaahhhh Sweet child of mine"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response