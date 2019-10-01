import json
import requests


def hello(event, context):
    body = {
        "body": requests.get('https://www.keithrozario.com/index.html').text
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
