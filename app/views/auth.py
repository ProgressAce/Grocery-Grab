# Views for authentication
from flask import Blueprint, jsonify, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models.user import User
from urllib.parse import urlsplit


auth_bl = Blueprint('auth', __file__)

@auth_bl.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Log-in page for registered users.

    TODO: GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    if request.method == 'GET':
        # return redirect(url_for('login'))  # for frontend
        return jsonify({'message': 'Use POST request '
                        + f'for {request.endpoint} endpoint'}), 400
    if current_user.is_authenticated:
        print('current user:', current_user.username)
        return jsonify({'message': 'Already logged in.'}), 200

    data: dict = request.get_json()

    if not data:
        return jsonify({'error': 'No user data provided'}), 400

    username = data.get('username')
    password = data.get('password')
    remember_me = request.args.get('remember_me') or False

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    if not password:
        return jsonify({'error': 'Password is required'}), 400

    user: User = User.objects(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=bool(remember_me))

        # moves to the original page if user was redirected to login
        # urlsplit().netloc used to determine if the next value is absolute or relative
        # to ensure only relative paths (paths within this app)
        # are redirected to and not a potentially malicious site
        next_page = request.args.get('next')  # Flask-Login will save origin page
        if not next_page or urlsplit(next_page).netloc != '':
            # next_page = url_for('index')
            return jsonify({'message': 'Logged in successfully'}), 200

        return redirect(next_page)

    return jsonify({'error': 'Incorrect username or password'}), 401


@auth_bl.route('/logout')
@login_required
def logout():
    """Sign-out a user."""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
