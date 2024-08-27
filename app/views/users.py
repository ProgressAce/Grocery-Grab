# Views for users
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from models.user import User
from app.utils.valid_data import is_valid_password


user_bl = Blueprint('users', __name__)

@user_bl.post('/users', strict_slashes=False)
def create_user():
    """POST a new user."""
    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()

        if not data:
            return jsonify({"error": "No user data provided"}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check if username and email are provided
        if not username:
            return jsonify({"error": "Username is required"}), 400

        if not email:
            return jsonify({"error": "Email is required"}), 400


        # Check if username and email already exist
        user_by_username = User.objects(username=username).first()
        user_by_email = User.objects(email=email).first()

        if user_by_username:
            return jsonify({'error': 'The username is already taken'}), 400

        if user_by_email:
            return jsonify({'error': 'The email is already taken'}), 400

        if not is_valid_password(password):
            return jsonify({'error': 'Password must be at least 8 characters long'
                            + ' and meet complexity requirements'}), 400

        password_hash = generate_password_hash(password)

        # TODO: implement verification of a new user via email
        # TODO: implement utility functions to catch exceptions and handle them by
        # sending an error return value
        user = User(username=username, email=email, password_hash=password_hash)
        user.save()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bl.get('/users/me', strict_slashes=False)
@login_required
def get_specific_user():
    """GET the logged-in user's information.
    
    Just the user's username, household_id and created_at fields are
    returned.
    """
    return jsonify({
        'username': current_user.username,
        'household_id': str(current_user.household_id.id),
        'created_at': current_user.created_at,
    }), 200


@user_bl.patch('/users/me', strict_slashes=False)
@login_required
def update_user():
    """UPDATES the logged-in user's profile details.
    
    Only the username is allowed to be changed for this route.
    """
    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()
        update_count = 1  # the number of fields that are allowed to be changed

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')

        # ensure only certain fields are passed to be updated
        if update_count < len(data.keys()):
            return jsonify({'error': f'Only {update_count} required field/s can'
                            + ' be updated'}), 400

        # Check if username is provided
        if not username:
            return jsonify({"error": "Username is required"}), 400

        # Check if username and email already exist
        user_by_username = User.objects(username=username).first()

        if user_by_username:
            return jsonify({'error': 'The username is already taken'}), 400

        current_user.username = username
        current_user.save()

        return jsonify({"message": "User updated"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bl.patch('/users/me/change-password', strict_slashes=False)
@login_required
def change_password():
    """UPDATE the logged-in user's password.
    
    The password is hashed before storing back into the database.
    """
    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not current_password:
            return jsonify({'error': 'current_password is required'})
        
        if not new_password:
            return jsonify({'error': 'new_password is required'})
        
        if not confirm_password:
            return jsonify({'error': 'confirm_password is required'})

        if not current_user.check_password(current_password):
            return jsonify({"error": "current_password is incorrect"}), 400

        if not is_valid_password(new_password):
            return jsonify({'error': 'new_password must be at least 8 characters long'
                            + ' and meet complexity requirements'}), 400

        if new_password != confirm_password:
            return jsonify({'error': 'New password and confirm password'
                            + ' do not match.'}), 400

        password_hash = generate_password_hash(new_password)

        current_user.password_hash = password_hash
        current_user.save()

        return jsonify({"message": "User updated"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
