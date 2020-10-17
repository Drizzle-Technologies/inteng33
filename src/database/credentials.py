import os


def access_credentials():
    credentials = os.environ['DATABASE_URL']

    print('Credentials loaded.')

    return credentials
