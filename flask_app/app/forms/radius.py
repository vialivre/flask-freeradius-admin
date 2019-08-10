from app import app
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    SelectField
)
from wtforms.validators import DataRequired

from app.utils import read_vendors

class NasForm(FlaskForm):
    VENDORS = read_vendors(app.config.get('DICTIONARIES_PATH'))

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