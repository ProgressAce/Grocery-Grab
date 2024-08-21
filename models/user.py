# Describes the schema of a `user` document
from datetime import datetime, UTC
from flask_login import UserMixin
from mongoengine import Document, ReferenceField, StringField, EmailField, \
                        EmbeddedDocument, EmbeddedDocumentListField, \
                        BooleanField, DateTimeField
from werkzeug.security import check_password_hash


class ShoppingListItem(EmbeddedDocument):
    item_name = StringField(max_length=200, required=True)
    added_date = DateTimeField(default=datetime.now(UTC))
    bought_date = DateTimeField(default=None)  # should not be less than added_date
    is_bought = BooleanField(default=False)


class User(UserMixin, Document):
    """Represents a user document in the user collection."""
    username = StringField(unique=True, max_length=60, min_length=2, required=True)
    email = EmailField(unique=True, required=True)
    password_hash = StringField(max_length=256, min_length=10, required=True)
    household_id = ReferenceField('Household',
                    help_text='A Foreign key representing a household\'s id ' +
                              'from the `household` collection')
    personal_shopping_list = EmbeddedDocumentListField(ShoppingListItem)

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
