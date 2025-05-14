from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators,  TextAreaField

class LoginForm(FlaskForm):
    username = StringField('USERNAME', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.Length(min=4, max=69)])
    submit =  SubmitField("Sign in")
    remember_me = BooleanField("Remember Me")

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired(), validators.Length(max=80)])
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[validators.DataRequired()])
    instructions = TextAreaField('Instructions', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField( 'Username', validators=[validators.DataRequired(), validators.Length(min=3, max=32)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=4, max=69)])
    submit = SubmitField('Register')
