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
