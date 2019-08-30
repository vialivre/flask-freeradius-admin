from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    user = StringField(
        _l('Username or Email'), 
        validators=[DataRequired(_l('This field is required.'))]
    )
    password = PasswordField(
        _l('Password'),
        validators=[DataRequired(_l('This field is required.'))]
    )
    remember = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Login to Dashboard'))