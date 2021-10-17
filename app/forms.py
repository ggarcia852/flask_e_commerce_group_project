from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp


class UserInfoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class AddItem(FlaskForm):
    hours = IntegerField('Hours')
    # submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Ranger(FlaskForm):
    color = StringField('Color', validators=[DataRequired()])
    skill = StringField('Skill', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = StringField('Image Source', validators=[DataRequired()])
    price = StringField('price', validators=[DataRequired()])
    submit = SubmitField('Add Ranger')

