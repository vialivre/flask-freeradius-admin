from app import app
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    SelectField,
    HiddenField,
    PasswordField,
    BooleanField
)
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

from app.utils import OPERATORS, read_vendors

DICTIONARIES_PATH = app.config.get('DICTIONARIES_PATH')

class NoValidationSelectField(SelectField):
    def pre_validate(self, form):
        return True
    def post_validate(self, form, validation_stopped):
        return True

class NasForm(FlaskForm):
    VENDORS = read_vendors(DICTIONARIES_PATH)

    name = StringField(
        _l('Name'),
        validators=[DataRequired(_l('This field is required.'))]
    )
    server = StringField(
        _l('Server'),
        validators=[DataRequired(_l('This field is required.'))]
    )
    ports = IntegerField(
        _l('Ports')
    )
    secret = StringField(
        _l('Secret'),
        validators=[DataRequired(_l('This field is required.'))]
    )
    short_name = StringField(_l('Short Name'))
    type = SelectField(_l('Type'), choices=VENDORS or [])
    custom_type = StringField(_l('Type'))
    community = StringField(_l('Community'))
    description = TextAreaField(_l('Description'))
    submit = SubmitField(_l('Submit'))


class GroupForm(FlaskForm):
    name = StringField(
        _l('Group Name'),
        validators=[DataRequired(_l('This field is required.'))]
    )
    description = TextAreaField(_l('Description'))
    submit = SubmitField(_l('Submit'))


class UserForm(FlaskForm):
    username = StringField(
        _l('Username'),
        validators=[DataRequired(_l('This field is required.'))]
    )
    email = StringField(_l('Email'))
    password = PasswordField(_l('Password'))
    active = BooleanField(_l('Active'), default=True)
    group = SelectField(_l('Group'), choices=[])
    name = StringField(_l('Name'))
    phone = StringField(_l('Phone'))
    address = TextAreaField(_l('Address'))
    has_access = BooleanField(_l('Can login into this system?'), default=False)


class AttributeForm(FlaskForm):
    VENDORS = read_vendors(DICTIONARIES_PATH)

    vendor = NoValidationSelectField(
        _l('Vendor'), choices=VENDORS or [],
        id='vendor_field'
    )
    
    attribute = NoValidationSelectField(
        _l('Attribute'), choices=[],
        validators=[DataRequired(_l('This field is required.'))],
        id='attribute_field'
    )
    custom_attribute = StringField(_l('Attribute'), id='custom_attribute_field')
    
    operation = SelectField(
        _l('Operation'), choices=OPERATORS,
        validators=[DataRequired(_l('This field is required.'))]
    )
    
    value = NoValidationSelectField(_l('Value'), choices=[], id='value_field')
    custom_value = StringField(_l('Value'), id='custom_value_field')

    processed_fields = HiddenField(
        _l('Processed Fields'), id='proc_fields',
        default='ca-cv'
    )