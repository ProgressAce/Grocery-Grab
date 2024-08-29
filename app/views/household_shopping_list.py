"""Views for a household's shopping list."""
from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models.household import Household, ShoppingListItem
from models.user import User
from app.utils.household_middleware import household_member_required

household_shopping_list_bl = Blueprint('household shopping list', __name__)


@household_shopping_list_bl.post('/households/shopping_list/items', strict_slashes=False)
@login_required
@household_member_required
def add_shopping_list_item():
    """GET the shopping list of a user's household.
    
    Middleware:
        - Ensures that the request was made by a logged-in user.
        - Ensures that the request was made by a user that belongs to
        a household.

    Nothing is done to prevent an item of the same name being added. Unlikely,
    but a user might want to add three items of the same name to buy separately.
    Eg. For buy a box of tennis balls once a week for four weeks as buying it
    in one go will not work for a household's budget.
    """
    household: Household = current_user.household_id

    try:
        # TODO: catch exception when given type of not application/json
        data: dict = request.get_json()

        if not data:
            return jsonify({"error": "No item data provided"}), 400

        item_name = data.get('item_name')

        # Check if the house name is provided
        if not item_name:
            return jsonify({"error": "The `item_name` is required"}), 400

        item = ShoppingListItem(
            item_name=item_name,
            added_by_user=current_user
        )

        household.shopping_list.append(item)
        household.save()

        return jsonify({"message": "Item added to shopping list successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


