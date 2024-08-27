"""Defines middleware for views associate to households."""
from flask import jsonify
from flask_login import current_user
from functools import wraps
from models.household import Household

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


def household_admin_required(view_func):
    """Middleware to protect a household route only admins should access."""
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        """Performs checks before allowing a user to access a household route.

        - Ensure that the user is logged in.
        - Ensure that the user is an admin of their household.
        """
        # Check that the user is logged in
        if not current_user:
            return jsonify({'error': 'User is not logged in'}), 400

        # Ensure that the user is a household admin
        household = current_user.household_id

        if current_user not in household.admins:
            return jsonify({'error': 'Only household admins are allowed to'
                            + 'change their household profile'})

        return view_func(*args, **kwargs)
    return decorated_function