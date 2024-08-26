# Describes the schema of a `household` document
from datetime import datetime, UTC
from mongoengine import Document, ReferenceField, StringField, ListField, \
                        EmbeddedDocument, EmbeddedDocumentListField, \
                        BooleanField, DateTimeField


class ShoppingListItem(EmbeddedDocument):
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
    
    users = ListField(ReferenceField('User'),
                    help_text='A list of users representing a user\'s id from'
                            + ' the `user` collection')
    
    shopping_list = EmbeddedDocumentListField(ShoppingListItem)
    created_at = DateTimeField(default=datetime.now(UTC))
    updated_at = DateTimeField(default=datetime.now(UTC))
