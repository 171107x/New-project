from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, TextField, SelectField
from wtforms.validators import DataRequired, Email, Length, equal_to

class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your username.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter your email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your passwords"),Length(min=6, message="Passwords must be 6 characters or more")])
    region = SelectField(
        choices=[('', 'Select'), ('North', 'North'), ('South', 'South'), ('East', 'East'),
                 ('West', 'West')], validators=[DataRequired('Please choose the region you are living in')])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Sign up')

class LoginForm(Form):
    username = StringField('', validators=[DataRequired("Please enter your username")])
    password = PasswordField('', validators=[DataRequired("Please enter a password")])
    submit = SubmitField('Sign in')

class EditForm(Form):
    username = StringField('', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired("Please enter your email address"),Email("Please enter your email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class ReviewForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')
