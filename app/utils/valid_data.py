"""Defines functions that handle the validation of data."""


def is_valid_password(password):
    """Validates the given password.

    TODO: Follow proper OWASP protocols.
    Returns:
        None, if invalid
        1, if it is valid
    """
    if not password or not isinstance(password, str):
        return None

    if len(password) < 8:
        return None

    return 1
