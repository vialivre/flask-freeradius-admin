from app import app
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    SelectField,
    HiddenField
)
from wtforms.validators import DataRequired

from app.utils import OPERATORS, read_vendors

DICTIONARIES_PATH = app.config.get('DICTIONARIES_PATH')

class NoValidationSelectField(SelectField):
    def pre_validate(self, form):
        return True
    def post_validate(self, form, validation_stopped):
        return True

class NasForm(FlaskForm):
    VENDORS = read_vendors(DICTIONARIES_PATH)

    name = StringField('Name', validators=[DataRequired()])
    server = StringField('Server', validators=[DataRequired()])
    ports = IntegerField('Ports', validators=[DataRequired()])
    secret = StringField('Secret', validators=[DataRequired()])
    short_name = StringField('Short Name')
    type = SelectField('Type', choices=VENDORS or [])
    custom_type = StringField('Type')
    community = StringField('Community')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class AttributeForm(FlaskForm):
    VENDORS = read_vendors(DICTIONARIES_PATH)

    vendor = NoValidationSelectField(
        'Vendor', choices=VENDORS or [],
        id='vendor_field'
    )
    
    attribute = NoValidationSelectField(
        'Attribute', choices=[],
        validators=[DataRequired()], id='attribute_field'
    )
    custom_attribute = StringField('Attribute', id='custom_attribute_field')
    
    operation = SelectField(
        'Operation', choices=OPERATORS,
        validators=[DataRequired()]
    )
    
    value = NoValidationSelectField('Value', choices=[], id='value_field')
    custom_value = StringField('Value', id='custom_value_field')

    processed_fields = HiddenField(
        'Processed Fields', id='proc_fields',
        default='ca-cv'
    )