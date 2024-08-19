# Setup code shared across multiple test files
import pytest
from app import create_app
from mongoengine import connect, disconnect

@pytest.fixture(scope='module')
def test_connections():
    """Initialises the testing environment for other tests.

    Flask app and database are setup for testing.
    """
    flask_app = create_app('test')  # the app's config specific for testing
    testing_client = flask_app.test_client()  # flask client for tests

    test_db_name = flask_app.config.get('MONGODB_SETTINGS').get('db')
    db = connect(test_db_name, 'test_connection')
    db.drop_database(test_db_name)

    with flask_app.app_context():
        yield testing_client

    disconnect()
