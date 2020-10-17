import json
import os


class Credentials:

    default_cpath = os.path.abspath('instance/auths/credentials.json')

    def __init__(self, cpath=default_cpath):

        with open(cpath) as f:
            c = json.load(f)

        self.__host = c['host']
        self.__db = c['db']
        self.__port = c['port']
        self.__user = c['user']
        self.__password = c['password']

        print('Credentials loaded.')

    def create_access_string(self):
        return f'postgres://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__db}'
