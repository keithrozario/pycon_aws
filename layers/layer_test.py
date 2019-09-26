import requests


def main(event, context):

    response = requests.get('https://www.keithrozario.com')

    return response.status_code


if __name__ == '__main__':

    print(main({}, {}))
