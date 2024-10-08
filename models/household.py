# Describes the schema of a `household` document
from datetime import datetime, UTC
from mongoengine import Document, ReferenceField, StringField, ListField, \
                        EmbeddedDocument, EmbeddedDocumentListField, \
                        BooleanField, DateTimeField, UUIDField
from uuid import uuid4
from werkzeug.security import check_password_hash


class ShoppingListItem(EmbeddedDocument):
    item_id = UUIDField(binary=False, primary_key=True, default=lambda: str(uuid4()))
    item_name = StringField(max_length=200, required=True)
    added_date = DateTimeField(default=datetime.now(UTC))
    bought_date = DateTimeField(default=None)  # should not be less than added_date
    is_bought = BooleanField(default=False)
    added_by_user = ReferenceField('User', required=False)
    bought_by_user = ReferenceField('User', required=False)


class Household(Document):
    """Represents a household document in the user collection."""
    name = StringField(max_length=60, min_length=2, required=True)

    password_hash = StringField(max_length=256, min_length=10, required=True,
                    help_text='Should only be used for initially joining the house.'
                            + ' No need to remember this password for frequent'
                            + ' authorization checks.')
    
    members = ListField(ReferenceField('User'),
                    help_text='A list of users representing a user\'s id from'
                            + ' the `user` collection')
    
    admins = ListField(ReferenceField('User'),
                    help_text='A list of users from `user` collection who have'
                            + ' admin privileges over the household.')
    
    shopping_list = EmbeddedDocumentListField(ShoppingListItem)
    created_at = DateTimeField(default=datetime.now(UTC))
    updated_at = DateTimeField(default=datetime.now(UTC))

    def check_password(self, password: str):
        """Determines if a password matches the hashed password of a user.

        Arg:
            password(str): the password to check.

        Returns:
            True if the password is valid, otherwise False.
        """
        return check_password_hash(self.password_hash, password)
