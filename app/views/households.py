"""Views for households."""
from app.utils.valid_data import is_valid_password
from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from functools import wraps
from models.household import Household
from werkzeug.security import generate_password_hash

household_bl = Blueprint('households', __name__)


def household_member_required(view_func):
    """Middleware to protect a household route."""
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        """Performs checks before allowing a user to access a household route.

        - Ensure that a user belongs to an existing household.
        - Ensure that the user is part of the household's members.
        """
        # Check if the user is part of a household
        if not current_user.household_id:
            return jsonify({'error': 'User is not part of a household'}), 400

        # Check if the user's household_id is valid and user is in the household
        household = Household.objects(id=current_user.household_id.id).first()
        if not household:
            return jsonify({'error': 'User\'s Household does not exist'}), 400

        if current_user not in household.members:
            return jsonify({'error': 'User is not a member of the'
                            + f' {household.name} Household.'}), 400

        # If everything is fine, proceed to the route
        return view_func(*args, **kwargs)
    return decorated_function


@household_bl.post('/households', strict_slashes=False)
@login_required
def create_household():
    """CREATE a new household."""

    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()

        if not data:
            return jsonify({"error": "No user data provided"}), 400

        name = data.get('name')
        password = data.get('password')

        # Check if the house name is provided
        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Ensure house name is unique
        user_by_username = Household.objects(name=name).first()
        if user_by_username:
            return jsonify({'error': 'The name is already taken'}), 400

        if not is_valid_password(password):
            return jsonify({'error': 'Password must be at least 8 characters long'
                            + ' and meet complexity requirements'}), 400

        password_hash = generate_password_hash(password)

        household = Household(name=name, password_hash=password_hash,
                              members=[current_user], admins=[current_user])
        household.save()
        current_user.household_id = household.id
        current_user.save()

        return jsonify({"message": "Household created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@household_bl.get('/households/our', strict_slashes=False)
@login_required
@household_member_required
def household_profile():
    """GET the household's profile details."""
    current_household: Household = current_user.household_id

    admin_usernames = [user.username for user in current_household.admins]
    member_usernames = [user.username for user in current_household.members]

    return jsonify({
        'household name': current_household.name,
        'admins': admin_usernames,
        'members': member_usernames,
        'created_at': current_household.created_at
    })
