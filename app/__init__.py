"""Project's main setup and configuration."""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from models.user import User
from app.views import index, users, auth, households, household_shopping_list
from mongoengine import connect
from mongoengine import errors
from pymongo.errors import ServerSelectionTimeoutError
from bson import ObjectId

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

    # TODO: account for mongo db not being active or connected properly
    # does not catch serverselectiontimeout error from mypongo
    try:
        # print('Connecting to mongo')
        connect(host=os.getenv(f'{env}_DATABASE'))
    except ServerSelectionTimeoutError as error:
        # print('Exception connecting to mongo db:', error.message)
        exit(1)

    config_class = config_classes[env]
    
    # Initialise flask app and load configuration depending on environment
    app = Flask(__name__)
    app.config.from_object(f'config.{config_class}')

    login_manager = LoginManager(app)

    # Setup the view to redirect to, for login
    login_manager.login_view = '/login'

    login_manager.login_message = 'Please login before accessing this resource.'

    @login_manager.user_loader
    def load_user(user_id) -> User:
        return User.objects(id=ObjectId(user_id)).first()

    app.register_blueprint(index.bl)
    app.register_blueprint(users.user_bl)
    app.register_blueprint(auth.auth_bl)
    app.register_blueprint(households.household_bl)
    app.register_blueprint(household_shopping_list.household_shopping_list_bl)

    return app
