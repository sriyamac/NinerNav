"""Contains functions for interacting with the user table.

All interaction with the user table should happen through these functions instead of via the User
class.
"""
from .models import db, User

def create_user(username: str, email: str, hash: str) -> User:
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

def get_user_by_username(username: str) -> User|None:
    """Gets a user by their username if they exist.

    Args:
        username: The username of the user to fetch

    Returns:
        The user with the given username if such a user exists
        None if no user has the given username
    """
    return User.query.filter_by(username=username).first()

def update_user_password(user: User, hash: str):
    """Updates a user's password with the newly provided hash.

    This function does not hash the password. Instead, it expects the provided paramter to already
    be a valid argon2 hash.

    Args:
        user: A User object that corresponds to an existing user
        hash: The new password hash for user
    """
    user.password = hash
    db.session.commit()