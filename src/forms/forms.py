from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class FormGame(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    console = StringField('Console', validators=[DataRequired()])
