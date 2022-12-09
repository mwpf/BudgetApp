from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    firstname = StringField("First Name")
    lastname = StringField("Last Name")
    email = EmailField("Email")
    password = PasswordField("Password")
    confirmpassword = PasswordField("ConfirmPassword")
    submit = SubmitField("Register")
