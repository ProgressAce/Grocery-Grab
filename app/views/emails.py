"""Views for email interaction."""
from app.utils.email_services import get_serializer, send_confirmation_email
from flask import Blueprint, current_app, jsonify
from flask_login import login_required, current_user
from itsdangerous import BadSignature, SignatureExpired
from models.user import User

email_bl = Blueprint('email_bl', __name__, url_prefix='/api')


@email_bl.get('/confirm_email/<token>')
def confirm_email(token):
    """Acknowledges that a user confirmed the registration of their new account
    """
    try:
        # decode the token to get the expected user email
        serializer = get_serializer()

        email = serializer.loads(
            token,
            salt=current_app.config.get('TOKEN_EMAIL_SALT'),
            max_age=int(current_app.config.get('TOKEN_EMAIL_AGE'))
        )

        user: User = User.objects(email=email).first()
        if not user:
            return jsonify({'error': 'User account does not exist'}), 500

        user.confirmed_email = True
        user.save()

        return jsonify({'message': 'Your email has been confirmed'}), 200
    except (BadSignature, SignatureExpired):
        return jsonify({'error': 'The confirmation token is invalid or expired'}), 400


@email_bl.get('/resend_email_confirmation')
@login_required
def resend_email_confirmation():
    """Sends an email to a user for then to confirm their email.
    """
    if current_user.confirmed_email:
        return jsonify({'message': 'User email is already confirmed'}), 400

    email_sent = send_confirmation_email(current_user.email)
    if not email_sent:
        return jsonify({'error': 'Unable to send the confirmation email'}), 400
    
    return jsonify({'message': 'Confirmation email sent'}), 200
