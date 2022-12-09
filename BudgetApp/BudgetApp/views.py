"""
Routes and views for the flask application.
"""

from flask import Flask, jsonify, redirect, url_for, request, render_template, flash
from datetime import date, datetime, timedelta
from BudgetApp import app
from BudgetApp.models.DbContext import *
from BudgetApp.plaid import *
import json
import plaid
import os
import time
import base64
import dateutil.parser as parser
from BudgetApp.forms import *

app.config["SECRET_KEY"] = "secretkey"


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    # if request.method == "POST":
    if form.validate_on_submit():
        # print("Form data:")
        # print("fname: {}, lname: {}".format(request.form.get("fname"), request.form.get("lname")))
        # flash("registration successfully completed for user {},{}".format(request.form.get("fname"),
        #                                                                   request.form.get("fname")), "success")
        print("Form data:")
        print("fname: {}, lname: {}".format(form.firstname.data, form.lastname.data))

        flash("registration successfully completed for user {},{}".format(form.firstname.data,
                                                                          form.lastname.data), "success")

        return redirect(url_for("login"))
    return render_template('register.html',
                           title='register', form=form)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html',
                           title='Login')


@app.route('/home')
def home():
    # get list of accounts
    db_accounts = account.query.join(plaid_item).filter_by(user_id=1).all()
    accounts_sch = account_schema(many=True)
    accounts = accounts_sch.dump(db_accounts)

    # get list of transactions
    db_transactions = transaction.query.all()
    transaction_sch = transaction_schema(many=True)
    transactions = transaction_sch.dump(db_transactions)

    # renders the dashboard
    return render_template(
        'index.html',
        title='Dashboard',
        month=datetime.now().month,
        year=datetime.now().year,
        accounts=accounts,
        transactions=transactions
    )


@app.route('/home/establish_item', methods=['POST'])
def establish_item():
    access_token = request.get_json()

    # /plaid/item/get
    item_response = get_item(access_token)

    # define new Plaid Item object and insert into db
    item = plaid_item(
        item_id=item_response.json['item']['item_id'],
        user_id=1,  # TODO : replace with logged in user's id
        institution_id=item_response.json['item']['institution_id'],
        webhook=item_response.json['item']['webhook'],
        request_id=item_response.json['request_id'],
        access_token=access_token,
        created_by='',
        created_date_time=date.today(),
        active=True
    )
    item.create()

    # /plaid/accounts/get
    account_response = get_accounts(access_token)

    # insert all accounts into db
    for acct in account_response.json['accounts']:
        # define new Account object and insert into db
        acct_obj = account(
            account_id=acct['account_id'],
            item_id=account_response.json['item']['item_id'],
            name=acct['name'],
            official_name=acct['official_name'],
            available_balance=acct['balances']['available'],
            current_balance=acct['balances']['current'],
            limit=acct['balances']['limit'],
            iso_currency_code=acct['balances']['iso_currency_code'],
            last_updated_date_time=date.today(),
            mask=acct['mask'],
            type=acct['type'],
            sub_type=acct['subtype'],
            verification_status=None,
            request_id=account_response.json['request_id'],
            active=True
        )
        acct_obj.create()

    # /plaid/transactions/get
    transaction_response = get_transactions(access_token)

    # insert transactions from last 30 days into db
    for txn in transaction_response.json['transactions']:
        # define new Transaction object and insert into db
        txn_obj = transaction(
            transaction_id=txn['transaction_id'],
            account_id=txn['account_id'],
            amount=txn['amount'],
            iso_currency_code=txn['iso_currency_code'],
            category_id=txn['category_id'],
            store_number=txn['location']['store_number'],
            payer=txn['payment_meta']['payer'],
            payee=txn['payment_meta']['payee'],
            reference_number=txn['payment_meta']['reference_number'],
            by_order_of=txn['payment_meta']['by_order_of'],
            payment_method=txn['payment_meta']['payment_method'],
            payment_processor=txn['payment_meta']['payment_processor'],
            reason=txn['payment_meta']['reason'],
            account_owner=txn['account_owner'],
            name=txn['name'],
            original_description=None,
            date=parser.parse(txn['date']).isoformat(),
            pending=txn['pending'],
            merchant_name=txn['merchant_name'],
            check_number=txn['check_number'],
            payment_channel=txn['payment_channel'],
            transaction_code=txn['transaction_code'],
            transaction_type=txn['transaction_type']
        )
        txn_obj.create()

    return redirect(url_for('home'))


@app.route('/budget')
def budget():
    # TODO : fill model
    return render_template(
        'budget.html'
    )


@app.route('/dbcontext/items', methods=['GET'])
def get_items():
    get_items = plaid_item.query.filter_by(user_id=1).all()
    item_schema = plaid_item_schema(many=True)
    items = item_schema.dump(get_items)
    return make_response(jsonify({"plaid_item": items}))
