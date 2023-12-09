"""Forms and validators to determine if authentication information provided by a user is valid.

This file contains wtforms that should be used to render templates and validate submitted user info
wherever possible.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, length, Regexp
from enum import Enum
from flask import Request
import re
from ..models import user as user_model

class FailureReason(Enum):
    UNKNOWN = "An unknown error has occured. Please try again."
    LONG_USERNAME = "Your username must be less than 100 characters."
    LONG_EMAIL = "Your email must be less than 100 charcters."
    BAD_EMAIL = "Your email is invalid. Please try again."
    SHORT_PASSWORD = "Your password must be at least 12 characters."
    NO_UPPER_PASSWORD = "Your password must have at least one uppercase character."
    NO_LOWER_PASSWORD = "Your password must have at least one lowercase character."
    DUPE_USERNAME = "Your username is already in use."
    DUPE_EMAIL = "Your email is already in use."

def find_user_failure_reason(request: Request) -> FailureReason:
    """Determines the reason that a user signup failed.

    This function assumes that the signup failed. If it succeeded, this function will return
    UNKNOWN.
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Do non-db checks first
    if len(username) > 100:
        return FailureReason.LONG_USERNAME

    if len(email) > 100:
        return FailureReason.LONG_EMAIL

    try:
        _is_valid_email(email)
    except ValidationError:
        return FailureReason.BAD_EMAIL

    if len(password) < 12:
        return FailureReason.SHORT_PASSWORD

    # No uppercase character
    if not re.match(".*[A-Z].*", password):
        return FailureReason.NO_UPPER_PASSWORD

    # No lowercase character
    if not re.match(".*[a-z].*", password):
        return FailureReason.NO_LOWER_PASSWORD

    # Check db for failure reasons
    if user_model.get_user_by_username(username) != None:
        return FailureReason.DUPE_USERNAME

    if user_model.get_user_by_email(email) != None:
        return FailureReason.DUPE_EMAIL

    return FailureReason.UNKNOWN

def _is_valid_email(value: FlaskForm|str, field=None):
    """Determines if a given email is valid.

    Args:
        value: The SignupForm that is being validated or an email as a str
        field: The field that is being validated

    Raises:
        wtforms.ValidationError: the provided field did not contain a valid email
    """
    if type(value) == SignupForm:
        email = field.data
    else:
        email = value

    # Verify that exactly one '@' is present
    if email.count("@") != 1:
        raise ValidationError("Missing @")

    # Verify that at least one '.' is present
    if email.count(".") == 0:
        raise ValidationError("Missing .")

    at_index = email.rfind("@")
    dot_index = email.rfind('.')

    # Verify that '@' is not the first character
    if at_index == 0:
        raise ValidationError("@ is first character")

    # Verify that '.' is not the last character
    if dot_index == len(email) - 1:
        raise ValidationError(". is last character")

    # Verify that there is a dot is after '@'
    if at_index > dot_index:
        raise ValidationError(". before @")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), length(max=100)])
    password = PasswordField("password", validators=[DataRequired()])

class SignupForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), length(max=100)])
    email = StringField("email", validators=[DataRequired(), length(max=100), _is_valid_email])
    password = PasswordField("password", validators=[DataRequired(), length(min=12), Regexp(".*[A-Z].*"), Regexp(".*[a-z].*")])

# Intentionally empty form, still uses wtforms' CSRF protection
class SignoutForm(FlaskForm):
    pass