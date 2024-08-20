"""Integration testing for the auth view."""
import flask.testing


# TestLogin:
def test_protected_route_redirect(test_connections):
    response = test_connections.get('/')
    assert response.status_code == 302
    print('(REMOVE) - location:', response.location)
    assert response.location == ''


def test_post_requirement(test_connections):
    response = test_connections.get('/login')
    expected_data = 'Use POST request for {request.endpoint} endpoint'
    assert response.status_code == 400
    assert response.data == expected_data


def test_no_data(test_connections):
    response = test_connections.post('/login')
    assert response.status_code == 400
    assert len(response.data) == 0
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{  }'
{
  "error": "No user data provided"
}
"""


def test_no_username(test_connections):
    response = test_connections.get('/login')
    expected_data = 'Use POST request for {request.endpoint} endpoint'
    assert response.status_code == 400
    assert response.data == expected_data
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "password": "MegaWord" }'
{
  "error": "Username is required"
}

curl localhost:5000/login -XPOST -H 'Content-Type: application/json' -d '{ "usernam": "AbacusWarrior" }'
{
  "error": "Username is required"
}
"""


def test_no_password(test_connections):
    response = test_connections.get('/login')
    expected_data = 'Use POST request for {request.endpoint} endpoint'
    assert response.status_code == 400
    assert response.data == expected_data
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "passwrd": "InuiTennis" }'
{
  "error": "Password is required"
}

curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "password": "" }'
{
  "error": "Password is required"
}
"""


def test_incorrect_credentials(test_connections):
    response = test_connections.get('/login')
    expected_data = 'Use POST request for {request.endpoint} endpoint'
    assert response.status_code == 400
    assert response.data == expected_data
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za", "password": "data" }'
{
  "error": "Password must be at least 8 characters long and meet complexity requirements"
}
"""


def test_successful_login(test_connections):
    response = test_connections.get('/login')
    expected_data = 'Use POST request for {request.endpoint} endpoint'
    assert response.status_code == 400
    assert response.data == expected_data
"""
curl localhost:5000/users -H "Content-Type: application/json" -XPOST -d '{ "username": "BurningSushiMan", "email": "taka@seigakutc.co.za", "password": "dataTennis" }'
{
  "error": "The username or email is already taken"
}
"""


def test_already_logged_in(test_connections):
    response = test_connections.get('/login')
    expected_data = 'Use POST request for {request.endpoint} endpoint'
    assert response.status_code == 400
    assert response.data == expected_data

"""
curl localhost:5000/login -H "Content-Type: application/json" -XPOST -d '{ "username": "AbacusWarrior", "email": "inui@seigakutc.co.za", "password": "dataTennis" }'
{
  "message": "User registered successfully"
}
"""