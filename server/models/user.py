"""Contains functions for interacting with the user table.

All interaction with the user table should happen through these functions instead of via the User
class.
"""
from .models import db, User

def create_user(username: str, email: str, hash: str) -> bool:
    """Creates a user with the provided information.

    Creates a new user based on the provided information. This function performs no validation, so
    any special requirements must be checked before this function is called.

    Args:
        username: The username of the new user
        email: The email of the new user
        hash: The argon2 hash of the new user's password

    Returns:
        The newly created user

    Raises:
        sqlalchemy.exc.IntegrityError: the username or email already correspond to an account
    """
    new_user = User(username=username, email=email, password=hash)
    db.session.add(new_user)
    db.session.commit()

    return new_user