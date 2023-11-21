"""A set of functions and classes to manage user sessions and authentication.

This file has funcitons to handle sign ups, log ins, and tracking user sessions. This file also
includes the User class, which enables storing information about sessions in a consistent format.
"""
from flask import request, Request
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.exc import IntegrityError
from .models import user as user_model, models

_ph = PasswordHasher()

def signup_user(request: Request) -> models.User|None:
    """Signs up a new user based on the provided request.

    Creates a new user using the provided request. request.form must have username, email, and
    password keys.

    Args:
        request: A flask.Request instance. request.form must have username, email, and password keys

    Returns:
        The user if the signup was successful
        None if the signup was unsuccessful

    Raises:
        ValueError: request.form did not have a username, email, or password key or the provided
            data is invalid
    """
    # TODO: add CSRF protection

    # Get the username, email, and password
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate the data
    if username == None or email == None or password == None:
        raise ValueError

    if len(username) > 100 or len(email) > 100:
        raise ValueError

    if not _is_valid_email(email):
        raise ValueError

    # TODO: create and enforce password requirements

    # Create the user, if possible
    try:
        return user_model.create_user(username, email, _ph.hash(password))
    except IntegrityError:
        return None

def login_user(request: Request) -> models.User|None:
    """Logs a user in based on the provided request.

    Determines if an account exists that corresponds with the username and password specified in
    request.form. request.form must have username and password keys.

    Args:
        request: A flask.Request instance. request.form must have username and password keys

    Returns:
        The user if the login was successful
        None if the login was unsuccessful

    Raises:
        ValueError: request.form did not have a username or password key or the provided
            data is invalid
    """
    # TODO: add CSRF protection

    # Get the username and password
    username = request.form.get("username")
    password = request.form.get("password")

    # Validate the data
    if username == None or password == None:
        raise ValueError

    if len(username) > 100:
        raise ValueError

    # Get the user by username if they exist
    user = user_model.get_user_by_username(username)

    if user == None:
        return None

    # Compare the provided password with the hash
    try:
        _ph.verify(user.password, password)
    except VerifyMismatchError:
        return None

    # Check if the hash needs to be updated, update if so
    if _ph.check_needs_rehash(user.password):
        user_model.update_user_password(user, _ph.hash(password))

    # User is authenticated, return them
    return user

def validate_user(request: Request) -> bool:
    """Determines if a given request is authenticated.

    Based on the request's session, this function determines if the request should be treated as
    authenticated.

    Args:
        request: A flask.Request instance

    Returns:
        True if the request is authenticated
        False if the request is unauthenticated
    """
    return False

class Session:
    """Holds information about a session in a consistent format.

    All information about a session should be stored here, including whether a session is
    authenticated, what their username is, and what their high score is.

    Attributes:
        is_authenticated: A boolean indicating if a session is authenticated
        username: A string indicating the user's username. None if the session is unauthenticated
    """

    def __init__(self, is_authenticated: bool=False, username: str|None=None):
        """Initializes the instance. The parameter defaults should only be overriden in extreme
        cases.

        Args:
            is_authenicated: Determines if a session is authenticated
            username: The username of the user of the session
        """
        self.is_authenticated = is_authenticated
        self.username = username

def _is_valid_email(email: str) -> bool:
    """Determines if a given email is valid.

    Args:
        email: The email to validate

    Returns:
        True if the email is valid
        False if the email is invalid
    """
    # Verify that exactly one '@' is present
    if email.count("@") != 1:
        return False

    # Verify that at least one '.' is present
    if email.count(".") == 0:
        return False

    at_index = email.rfind("@")
    dot_index = email.rfind('.')

    # Verify that '@' is not the first character
    if at_index == 0:
        return False

    # Verify that '.' is not the last character
    if dot_index == len(email) - 1:
        return False

    # Verify that there is a dot is after '@'
    return at_index < dot_index
