"""A set of functions to manage user sessions and authentication.

This file has funcitons to handle sign ups, log ins, and tracking user sessions. The keys added to
the session object are listed below.

* authenticated (bool) - true if the user is authenticated, false otherwise
* username (str) - the user's username
"""
from flask import Request, session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.exc import IntegrityError
import re
from ..models import user as user_model, models

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
    """
    # Get the username, email, and password
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

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
    """
    # Get the username and password
    username = request.form.get("username")
    password = request.form.get("password")

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

    # Mark the user's session as authenticated
    session["authenticated"] = True
    session["username"] = username

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
    if "authenticated" not in session:
        return False

    return session["authenticated"]