import os


class Configuration(object):
    DEBUG = True

    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = 'super secret key right here. Seriously, it is SECRET!'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/vvapp.db' % APPLICATION_DIR

    SQLALCHEMY_TRACK_MODIFICATIONS = True
