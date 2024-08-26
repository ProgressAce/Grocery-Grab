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
    REMEMBER_COOKIE_DURATION = timedelta(days=60)


class ProductionConfig(Config):
    """The flask configuration for a production environment."""
    DEBUG = False  # ensure debug mode is false


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
