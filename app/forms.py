from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(FlaskForm):
    usernameOrEmail = StringField(
        "Username Or Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember_me = BooleanField("Remember Me")
    loginButton = SubmitField("Log In")

class SignupForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    signupButton = SubmitField("Sign Up")
