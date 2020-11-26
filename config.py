import os


# default config
class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mandalorian'


# Unit test configurations
class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Development config
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    except KeyError as e:
        SQLALCHEMY_DATABASE_URI = ''


# Production config
class ProductionConfig(BaseConfig):
    DEBUG = False
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    except KeyError as e:
        SQLALCHEMY_DATABASE_URI = ''
