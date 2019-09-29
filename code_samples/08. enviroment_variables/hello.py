import json
import os


def main(event, context):

    body = {
        "env_var": os.environ['ENV_VAR'],
        "env_var_2": os.environ.get('ENV_VAR_2', 'n.a')
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response