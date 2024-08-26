"""Integration testing for the users view."""
import flask.testing


# TestRegistration:
def test_no_username(test_connections):
    response = test_connections.post('/users')
    assert response.status_code == 400
    assert len(response.data) == 0
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "email": "inui@seigakutc.co.za", "password": "data" }'
{
  "error": "Username is required"
}
"""


def test_no_email(test_connections):
    response = test_connections.put('/users')
    assert response.status_code == 405
    assert len(response.data) == 0
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za" }'
{
  "error": "Email is required"
}

curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za", "PASSWORD": "data" }'
{
  "error": "Email is required"
}
"""


def test_no_password(test_connections):
    response = test_connections.delete('/users')
    assert response.status_code == 405
    assert len(response.data) == 0
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za", "password": "" }'
{
  "error": "Password must be at least 8 characters long and meet complexity requirements"
}

curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za" }'
{
  "error": "Password must be at least 8 characters long and meet complexity requirements"
}
"""

# TODO: Must still implement owasp secure password
def test_invalid_password(test_connections):
    pass
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za", "password": "data" }'
{
  "error": "Password must be at least 8 characters long and meet complexity requirements"
}
"""


def test_unique_username(test_connections):
    """Ensures that the provided username will be unique in the database."""
    pass
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "BurningSushiMan", "email": "taka@seigakutc.co.za", "password": "dataTennis" }'
{
  "error": "The username or email is already taken"
}
"""


def test_unique_email(test_connections):
    """Ensures that the provided email will be unique in the database."""
    pass
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "ProudHorio", "email": "inui@seigakutc.co.za", "password": "dataTennis" }'
{
  "error": "The username or email is already taken"
}
"""

def test_successful_creation(test_connections):
    pass
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za", "password": "dataTennis" }'
{
  "message": "User registered successfully"
}
"""