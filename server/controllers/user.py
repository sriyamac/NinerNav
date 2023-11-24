from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, length, Regexp
import wtforms.validators as validators

def _is_valid_email(form, field):
    """Determines if a given email is valid.

    Args:
        form: The form that is being validated
        field: The field that is being validated

    Raises:
        wtforms.ValidationError: the provided field did not contain a valid email
    """
    email = field.data

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
    email = StringField("email", validators=[DataRequired(), _is_valid_email])
    password = PasswordField("password", validators=[DataRequired(), Regexp(".*[A-Z].*"), Regexp(".*[a-z].*")])