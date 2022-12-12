
from sqlalchemy import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, PasswordField, BooleanField, SubmitField, HiddenField, EmailField, SelectField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email
from BudgetApp.models.DbContext import *

"""

EXAMPLE:

class SignupForm(FlaskForm):
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )
    confirmPassword = PasswordField(
        'Repeat Password',
        [
            EqualTo(password, message='Passwords must match.')
        ]
    )
    title = SelectField(
        'Title',
        [DataRequired()],
        choices=[
            ('Farmer', 'farmer'),
            ('Corrupt Politician', 'politician'),
            ('No-nonsense City Cop', 'cop'),
            ('Professional Rocket League Player', 'rocket'),
            ('Lonely Guy At A Diner', 'lonely'),
            ('Pokemon Trainer', 'pokemon')
        ]
    )
    website = StringField(
        'Website',
        validators=[URL()]
    )
    birthday = DateField('Your Birthday')
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

"""

class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!")
        ]
    )
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    def validate_email(self, email):
        usr = user.query.filter_by(email=email.data).first()
        if usr is not None:
            raise ValidationError('Please use a different email address.')

class BudgetForm(FlaskForm):
    budget_id = HiddenField('Budget ID', validators=[DataRequired()])
    user_id = HiddenField('User ID', validators=[DataRequired()])
    month = StringField('Month', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    created_date_time = DateField('Created DateTime', validators=[DataRequired()])

class BudgetItemForm(FlaskForm):
    budget_item_id = HiddenField('Budget Item ID', validators=[DataRequired()])
    budget_item_type_id = HiddenField('Budget Item Type ID', validators=[DataRequired()])
    budget_id = HiddenField('Budget ID', validators=[DataRequired()])
    fixed = BooleanField('Fixed')
    due_date = DateField('Due Date')
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    projected_amount = DecimalField('Projected Amount', validators=[DataRequired()])
    actual_amount = DecimalField('Actual Amount')
    category_id = IntegerField('Category ID')
    sub_category_id = IntegerField('Sub-Category ID')

class TransactionForm(FlaskForm):
    transaction_id = HiddenField('Transaction ID', validators=[DataRequired()])
    account_id = SelectField('Account')
    amount = DecimalField('Amount')
    iso_currency_code = SelectField('ISO Currency Code', choices=[('USD', 'USD')])
    category_id = StringField('Category ID')
    store_number = StringField('Store Number')
    payer = StringField('Payer')
    payee = StringField('Payee')
    reference_number = StringField('Reference Number')
    by_order_of = StringField('By Order Of')
    payment_method = StringField('Payment Method')
    payment_processor = StringField('Payment Processor')
    reason = StringField('Reason')
    account_owner = StringField('Account Owner')
    name = StringField('Name')
    original_description = StringField('Original Description')
    date = DateField('Date')
    pending = BooleanField('Pending')
    merchant_name = StringField('Merchant Name')
    check_number = StringField('Check Number')
    payment_channel = StringField('Payment Channel')
    transaction_code = StringField('Transaction Code')
    transaction_type = StringField('Transaction Type')

# HELPERS
#region

#endregion