from flask_wtf import Form
from wtforms import  StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your username.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter your email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your passwords"),Length(min=6, message="Passwords must be 6 characters or more")])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Sign up')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your username")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address"),Email("Please enter your email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    submit = SubmitField('Sign in')

class EditForm(Form):
    username = StringField('nickname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired("Please enter your email address"),Email("Please enter your email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

