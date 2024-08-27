"""Views for email interaction."""
from app.utils.email_services import get_serializer, send_confirmation_email
from flask import Blueprint, current_app, jsonify
from flask_login import login_required, current_user
from itsdangerous import BadSignature, SignatureExpired
from models.user import User

email_bl = Blueprint('email_bl', __name__)


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
