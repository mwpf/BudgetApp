from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email

class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=3, max=20, message="First name must be between 2 and 20 characters long")
                                ])
    lastname = StringField("Last Name", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=3, max=20, message="Last Name must be between 3 and 20 characters long")
                                ])
    email = EmailField("Email", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=30, message="Email must be between 5 and 30 characters long"),
                                    Email("You did not enter a valid email!")
                                ])
    password = PasswordField("Password", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=40, message="Password must be between 10 and 40 characters long"),
                                    EqualTo("password_confirm", message="Passwords must match")
                                ])
    confirmpassword = PasswordField("ConfirmPassword", validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!")
                                ])
    submit = SubmitField("Register")
