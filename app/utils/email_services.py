"""Handles all the app's mailing functionality."""
from app.extensions import mail
from flask import current_app, url_for
from flask_mail import Message


def get_serializer():
    """Get the app's shared serializer.
    
    The serializer is used for token generation and validation. It ensures the
    data is cryptographically signed to prevent tampering and it can also be
    used to retrieve the untampered data that was used to generate the token.
    """
    return current_app.config.get('TOKEN_SERIALIZER')


def send_confirmation_email(user_email: str):
    """Emails a user and provides a link they can access for a certain task.

    Examples of links can include, confirmation link for a user acknowledging
    their registration, a password reset link, etc.
    """
    try:
        token = generate_url_token(user_email)

        msg = Message('Confirm Email', recipients=[user_email])
        link = url_for('email_bl.confirm_email', token=token, _external=True)
        msg.body = f'Please confirm your email by clicking on the following link: {link}'

        mail.send(msg)
    except Exception as exc:
        print(exc)
        return 0

    return 1


def generate_url_token(user_email: str):
    """Generates a unique token id for a URL.
    
    Arg:
        user_email: the email address of a user.

    Dependencies:
        - Uses the `itsdangerous` package's `URLSafeTimedSerializer` class
        to get a string serialized object that can be used for a URL. 
        
    The string serialized object will be used to encode an email with a
    salt value. This encoding will serve as the token for a URL.

    The salt value is used to decode the token so it should be kept a secret.
    """
    if not user_email:
        return None

    salt = current_app.config.get('TOKEN_EMAIL_SALT')
    serializer = get_serializer()

    token = serializer.dumps(user_email, salt=salt)

    return token
