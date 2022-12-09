from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email
from BudgetApp.models.DbContext import user

def user_exists_with_email(form, field):
    cur_user = user.query.filter_by(email=field.data.lower()).first()
    if not cur_user:
        raise ValidationError("There is no registered account with that email.")

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
        EqualTo("confirmpassword", message="Passwords must match")
    ])
    confirmpassword = PasswordField("ConfirmPassword", validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!")
    ])
    submit = SubmitField("Register")
    def validate_email(form, field):
        cur_user = user.query.filter_by(email=field.data.lower()).first()
        if cur_user:
            raise ValidationError("Email already exists.")

    class LoginForm(FlaskForm):
        email = EmailField("Email",
                           validators=[
                               InputRequired("Input is required!"),
                               DataRequired("Data is required!"),
                               Length(min=10, max=30, message="Email must be between 5 and 30 characters long"),
                               user_exists_with_email
                           ])
        password = PasswordField("Password",
                                 validators=[
                                     InputRequired("Input is required!"),
                                     DataRequired("Data is required!"),
                                     Length(min=10, max=40,
                                            message="Password must be between 10 and 40 characters long")
                                 ])
        submit = SubmitField("Login")
