"""Unit tests to ensure conftest provides all the expected pytest config"""
#from tests.conftest import test_connections
import flask.testing


def test_client_is_instance_of_test_client(test_connections):
    assert isinstance(test_connections, flask.testing.FlaskClient)
