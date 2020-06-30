
import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False



TESTING = True
DEBUG = True

APP_ENV = 'testing'

WTF_CSRF_ENABLED = False
