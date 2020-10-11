from os import environ


class Config:
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = environ.get('SECRET_KEY')
