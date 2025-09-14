from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class FormGame(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    console = StringField('Console', validators=[DataRequired()])


class FormUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
