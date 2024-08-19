# Views for users
from flask import Blueprint
from werkzeug.security import generate_password_hash
from flask import jsonify, request
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
