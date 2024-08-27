"""Defines the app's Environment-Specific Configuration for Flask."""
from os import environ, path
from datetime import timedelta
from dotenv import load_dotenv

# Specify the .env file containing the key/value config values
base_dir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_dir, '.env'))


class Config(object):
    """The base setup for a Flask app's configuration."""
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    # Email configuration for development and testing
    MAIL_SERVER = environ.get('DEV-MAIL_SERVER')
    MAIL_PORT = environ.get('DEV-MAIL_PORT')
    MAIL_USE_TLS = False  # No TLS for local testing
    MAIL_USE_SSL = False  # No SSL for local testing
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'dummy@grocery_squad.com'
    MAIL_DEBUG = 1

    # Token security for development and testing
    TOKEN_EMAIL_SALT = environ.get('DEV_TOKEN_EMAIL_SALT')
    TOKEN_EMAIL_AGE = environ.get('DEV_TOKEN_EMAIL_AGE')


class ProductionConfig(Config):
    """The flask configuration for a production environment."""
    DEBUG = False  # ensure debug mode is false

    MAIL_SERVER = environ.get('PROD-MAIL_SERVER')
    MAIL_PORT = environ.get('PROD-MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('PROD-MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('PROD-MAIL_PASSWORD')
    MAIL_DEBUG = 0

    TOKEN_EMAIL_SALT = environ.get('PROD_TOKEN_EMAIL_SALT')
    TOKEN_EMAIL_AGE = environ.get('PROD_TOKEN_EMAIL_AGE')


class DevelopmentConfig(Config):
    """The flask configuration for a development environment."""
    DEBUG = environ.get('DEBUG')


class TestingConfig(Config):
    """The flask configuration for a testing environment."""
    TESTING = environ.get('TESTING')
    DEBUG = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False  # Prevents exceptions from propagating
    # a separate database for tests
    # the test database's connection name is stored in the .env file
    MONGODB_SETTINGS = {
        'db': environ.get('TEST_DB'),
    }
