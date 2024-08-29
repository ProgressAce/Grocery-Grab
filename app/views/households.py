"""Views for households."""
from app.utils.valid_data import is_valid_password
from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models.household import Household
from models.user import User
from app.utils.household_middleware import household_member_required, \
    household_admin_required
from werkzeug.security import generate_password_hash

household_bl = Blueprint('households', __name__)


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


@household_bl.get('/households/profile', strict_slashes=False)
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


@household_bl.patch('/households/profile/name', strict_slashes=False)
@login_required
@household_member_required
@household_admin_required
def change_household_name():
    """UPDATES a household's username field.

    The specified household belongs to the logged-in user making the request.
    Only a user that is a household admin will be able to change their
    household's profile details.
    Only the username is allowed to be changed for this route.
    """
    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')

        # Check if name is provided
        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Check if household name already exists
        household_by_name = Household.objects(name=name).first()

        if household_by_name:
            return jsonify({'error': 'The household name is already taken'}), 400

        household = current_user.household_id
        household.name = name
        household.save()

        return jsonify({"message": "Household name is updated"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@household_bl.post('/households/join', strict_slashes=False)
@login_required
def join_household():
    """Adds a user to a household.
    
    The household ID and password are expected to be entered correctly by
    the user.
    """
    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        household_id = data.get('id')
        password = data.get('password')

        # Check if name is provided
        if not household_id:
            return jsonify({"error": "Household `id` is required"}), 400
        
        if not password:
            return jsonify({"error": "Password is required"}), 400

        # Check if household exists
        household: Household = Household.objects(id=ObjectId(household_id)).first()

        if not household:
            return jsonify({'error': 'The household you entered does not exist'}), 400
        
        if not household.check_password(password):
            return jsonify({'message': 'Incorrect password.'}), 401

        if current_user in household.members:
            return jsonify({'error': 'User is already part of this household'}), 400

        household.members.append(current_user)
        current_user.household_id = household
        household.save()
        current_user.save()

        return jsonify({'message': f'Household "{household.name}" joined successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@household_bl.delete('/households/members/<user_id>', strict_slashes=False)
@login_required
@household_member_required
@household_admin_required
def remove_household_member(user_id: str):
    """REMOVES a household member.

    Middleware:
        - ensures the request comes from a logged-in user.
        - ensures the user belongs to a household and the household exists.
        - ebsures only admins accesses this route.

    The specified household belongs to the logged-in user making the request.
    Only a user that is a household admin will be able to remove a household
    member from their household.

    The household admin would need to give the username of the user they want
    to remove.
    The household's and the user's affiliation with each other will be removed.
    """
    try:
        user: User = User.objects(id=ObjectId(user_id)).first()
        household: Household = current_user.household_id

        if user not in household.members:
            return jsonify({'error': 'This user is not a member of the household'}), 400

        if user in household.admins:
            return jsonify({'error': 'Unable to remove a household admin'}), 401
    
        household.members.remove(user)
        user.household_id = None

        household.save()
        user.save()

        return jsonify({'message': 'User removed successfully'}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@household_bl.patch('/households/admins/<user_id>', strict_slashes=False)
@login_required
@household_member_required
@household_admin_required
def add_household_admin(user_id: str):
    """Updates a household member's status to household admin.

    Middleware:
        - ensures the request comes from a logged-in user.
        - ensures the user belongs to a household and the household exists.
        - ebsures only admins accesses this route.

    The specified household belongs to the logged-in user making the request.
    Only a user that is a household admin will be able to remove a household
    member from their household.

    The household admin is required to give the id of the user they want
    to promote to household admin. 
    Thus, the user will be added to the household's admin members.
    """
    try:
        user: User = User.objects(id=ObjectId(user_id)).first()
        household: Household = current_user.household_id

        if user not in household.members:
            return jsonify({'error': 'This user is not a member of the household'}), 400

        if user in household.admins:
            return jsonify({'error': 'This user is already an admin'}), 401

        household.admins.append(user)
        household.save()

        return jsonify({'message': 'User promoted to admin successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500