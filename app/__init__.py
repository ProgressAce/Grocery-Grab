"""Project's main setup and configuration."""
import os
from dotenv import load_dotenv
from flask import Flask
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models.user import User
from app.views import index, users, auth
from mongoengine import connect

config_classes = {
    'DEV': 'DevelopmentConfig',
    'TEST': 'TestingConfig',
    'PROD': 'ProductionConfig'
}

load_dotenv()


def create_app(environment=None):
    """The app's application factory performing the config and setup.
    """
    if not environment:
        environment = ''

    env = environment.upper()  # environment variable names are in upper case
    if env not in ['DEV', 'TEST', 'PROD']:
        env = 'DEV'  # this is the default execution environment

    connect(host=os.getenv(f'{env}_DATABASE'))

    config_class = config_classes[env]
    
    # Initialise flask app and load configuration depending on environment
    app = Flask(__name__)
    app.config.from_object(f'config.{config_class}')

    app.register_blueprint(index.bl)
    app.register_blueprint(users.user_bl)

    return app
