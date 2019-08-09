from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NasForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    server = StringField('Server', validators=[DataRequired()])
    ports = StringField('Ports', validators=[DataRequired()])
    secret = StringField('Secret', validators=[DataRequired()])
    short_name = StringField('Short Name')
    type = StringField('Type')
    community = StringField('Community')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')