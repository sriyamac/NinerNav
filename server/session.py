"""A set of functions and classes to manage user sessions and authentication.

This file has funcitons to handle sign ups, log ins, and tracking user sessions. This file also
includes the User class, which enables storing information about sessions in a consistent format.
"""
from flask import request, Request
from argon2 import PasswordHasher

_ph = PasswordHasher()

def signup_user(request: Request) -> bool:
    """Signs up a new user based on the provided request.

    Creates a new user using the provided request. request.form must have username and password
    keys.

    Args:
        request: A flask.Request instance. request.form must have username and password keys

    Returns:
        True if the user was created successfully
        False if the user was not created successfully

    Raises:
        ValueError: request.form did not have a username or password key
    """
    return False

def login_user(request: Request) -> bool:
    """Logs a user in based on the provided request.

    Determines if an account exists that corresponds with the username and password specified in
    request.form. request.form must have username and password keys.

    Args:
        request: A flask.Request instance. request.form must have username and password keys

    Returns:
        True if the user was logged in successfully
        False if the user was not logged in successfully

    Raises:
        ValueError: request.form did not have a username or password key
    """
    return False

def validate_user(request: Request) -> bool:
    """Determines if a given request is authenticated.

    Based on the request's session, this function determines if the request should be treated as
    authenticated.

    Args:
        request: A flask.Request instance. request.form must have username and password keys

    Returns:
        True if the request is authenticated
        False if the request is unauthenticated
    """
    return False

class User:
    """Holds information about a user in a consistent format.

    All information about a user or session should be stored here, including whether a session is
    authenticated, what their username is, and what their high score is.

    Attributes:
        is_authenticated: A boolean indicating if a session is authenticated
        username: A string indicating the user's username. None if the user is unauthenticated
    """

    def __init__(self, is_authenticated: bool=False, username: str|None=None):
        """Initializes the instance. The parameter defaults should only be overriden in extreme
        cases.

        Args:
            is_authenicated: Determines if a user is authenticated
            username: The username of the user
        """
        self.is_authenticated = is_authenticated
        self.username = username