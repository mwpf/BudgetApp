"""
Routes and views for the flask application.
"""

from flask import Flask, jsonify, redirect, url_for, request, render_template, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from datetime import date, datetime, timedelta
from werkzeug.urls import url_parse
from BudgetApp import app, login_manager
from BudgetApp.models.DbContext import *
from BudgetApp.models.forms import *
from BudgetApp.plaid import *
import dateutil.parser as parser
import calendar

# LOGIN / REGISTRATION
#region

@login_manager.user_loader
def load_user(id):
    return user.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        usr = user.query.filter_by(email=form.email.data).first()
        if usr is None or not usr.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(usr, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template(
        'login.html',
        title='Log In',
        form=form
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        usr = user(
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
            email = request.form['email'],
            active = 1
        )
        usr.set_password(request.form["password"])
        usr.create()
        flash('Registration Successful!')
        return redirect(url_for('login'))
    return render_template(
        'registration.html',
        title='Register',
        form=form
    )

#endregion

# DASHBOARD
#region

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def home():
    session.pop('_flashes', None)
    user_id = current_user.get_id()
    
    # get list of accounts
    db_accounts = account.query.join(plaid_item).filter_by(user_id=user_id).all()

    # get list of transactions from all accounts
    db_transactions = []
    for acct in db_accounts:
        db_transactions.extend(transaction.query.filter_by(account_id=acct.account_id).all())

    # renders the dashboard
    return render_template(
        'index.html',
        title='Dashboard',
        month=datetime.now().month,
        year=datetime.now().year,
        accounts=db_accounts,
        transactions=sorted(db_transactions, key=lambda t: t['date'], reverse=True) # TODO : will break if date is null
    )

@app.route('/home/establish_item', methods = ['POST'])
def establish_item():
    access_token = request.get_json()
    
    # /plaid/item/get
    item_response = get_item(access_token)

    # define new Plaid Item object and insert into db
    item = plaid_item(
        item_id = item_response.json['item']['item_id'],
        user_id = current_user.get_id(),
        institution_id = item_response.json['item']['institution_id'],
        webhook = item_response.json['item']['webhook'],
        request_id = item_response.json['request_id'],
        access_token = access_token,
        created_by = '',
        created_date_time = date.today(),
        active = True
    )
    item.create()
    
    # /plaid/accounts/get
    account_response = get_accounts(access_token)
    
    # insert all accounts into db
    for acct in account_response.json['accounts']:
        # define new Account object and insert into db
        acct_obj = account(
            account_id = acct['account_id'],
            item_id = account_response.json['item']['item_id'],
            name = acct['name'],
            official_name = acct['official_name'],
            available_balance = acct['balances']['available'],
            current_balance = acct['balances']['current'],
            limit = acct['balances']['limit'],
            iso_currency_code = acct['balances']['iso_currency_code'],
            last_updated_date_time = date.today(),
            mask = acct['mask'],
            type = acct['type'],
            sub_type = acct['subtype'],
            verification_status = None,
            request_id = account_response.json['request_id'],
            active = True
        )
        acct_obj.create()

    # /plaid/transactions/get
    transaction_response = get_transactions(access_token)
    
    # insert transactions from last 30 days into db
    for txn in transaction_response.json['transactions']:
        # define new Transaction object and insert into db
        txn_obj = transaction(
            plaid_transaction_id = txn['transaction_id'],
            account_id = txn['account_id'],
            amount = txn['amount'],
            iso_currency_code = txn['iso_currency_code'],
            category_id = txn['category_id'],
            store_number = txn['location']['store_number'],
            payer = txn['payment_meta']['payer'],
            payee = txn['payment_meta']['payee'],
            reference_number = txn['payment_meta']['reference_number'],
            by_order_of = txn['payment_meta']['by_order_of'],
            payment_method = txn['payment_meta']['payment_method'],
            payment_processor = txn['payment_meta']['payment_processor'],
            reason = txn['payment_meta']['reason'],
            account_owner = txn['account_owner'],
            name = txn['name'],
            original_description = None,
            date = parser.parse(txn['date']).isoformat(),
            pending = txn['pending'],
            merchant_name = txn['merchant_name'],
            check_number = txn['check_number'],
            payment_channel = txn['payment_channel'],
            transaction_code = txn['transaction_code'],
            transaction_type = txn['transaction_type']
        )
        txn_obj.create()

    return redirect(url_for('home'))

@app.route('/manual_transaction', methods=['GET', 'POST'])
def manual_transaction():
    
    # get optional arguments
    transaction_id = request.args.get('transaction_id')

    if transaction_id is not None: 
        form.transaction_id.data = transaction_id

    form = TransactionForm(request.form)
    
    # populate account choices
    form.account_id.choices = [(a.account_id, a.name) for a in account.query.join(plaid_item).filter_by(user_id=current_user.get_id()).all()]

    if request.method == 'POST':
        if form.is_submitted():
            if request.form["transaction_id"] is not None and not request.form["transaction_id"] == "":
                txn = transaction.query.get(request.form["transaction_id"])
                form.populate_obj(txn)
                txn.update()
            else:
                # create income budget item and insert into db
                txn = transaction(
                    account_id = request.form["account_id"],
                    name = request.form["name"],
                    amount = request.form["amount"],
                    date = request.form["date"]
                )
                txn.create()

            # TODO : create transaction detail for the category/subcategory selected

        return redirect(url_for('home'))

    else:
        # if transaction id was specified
        if transaction_id is not None:
            # grab the transaction from the database
            txn = transaction.query.get(transaction_id)
            form = TransactionForm(obj=txn)

        return render_template('_transaction.html', form=form)
    
#endregion

# BUDGET 
#region 

@app.route('/get_budget', methods=['GET', 'POST'], defaults={ 'budget_id': None })
@app.route('/get_budget/<budget_id>', methods=['GET'])
@login_required
def get_budget(budget_id):

    income_type_id = get_budget_item_type("Income")
    expense_type_id = get_budget_item_type("Expense")

    if request.method == 'POST':
        # TODO : implement budget creation
        return redirect(url_for('budget', budget_id=budget_id))

    else:
        # grab the budget specified
        if budget_id is not None:
            curr = budget.query.filter_by(budget_id=budget_id).one()

        # otherwise grab the most recent budget
        else:
            curr = budget.query.filter_by(user_id=current_user.get_id()).order_by(budget.created_date_time.desc()).first()
        
        # finally, if no budget can be found, create one for the current month & year
        if curr is None:
            curr = budget(
                user_id = current_user.get_id(),
                month = calendar.month_name[datetime.now().month],
                year = datetime.now().year,
                created_date_time = datetime.now()
            )
            curr.create()

        db_budgets = budget.query.filter_by(user_id=current_user.get_id()).all()
        db_incomes = budget_item.query.filter_by(budget_id=curr.budget_id, budget_item_type_id=income_type_id).all()
        db_expenses = budget_item.query.filter_by(budget_id=curr.budget_id, budget_item_type_id=expense_type_id).all()

        return render_template(
            'budget.html', 
            budget = curr,
            budgets = db_budgets,
            incomes = db_incomes,
            expenses = db_expenses
        )

@app.route('/income', methods=['GET', 'POST'])
def income():
    # get optional arguments
    budget_id = request.args.get('budget_id')
    budget_item_id = request.args.get('budget_item_id')

    # grab the id for Income item type
    type_id = get_budget_item_type("Income")

    form = BudgetItemForm(request.form)

    if budget_id is not None: 
        form.budget_id.data = budget_id
    if budget_item_id is not None: 
        form.budget_item_id.data = budget_item_id

    form.budget_item_type_id.data = type_id

    if request.method == 'POST':
        if form.is_submitted():
            if request.form["budget_item_id"] is not None and not request.form["budget_item_id"] == "":
                income = budget_item.query.get(request.form["budget_item_id"])
                form.populate_obj(income)
                income.update()

            else:
                # create income budget item and insert into db
                income = budget_item(
                    budget_item_type_id = type_id,
                    budget_id = request.form["budget_id"],
                    due_date = request.form["due_date"] if request.form["due_date"] != '' else None,
                    name = request.form["name"],
                    description = request.form["description"],
                    projected_amount = request.form["projected_amount"]
                    #category_id = request.form["category_id"],
                    #sub_category_id = request.form["sub_category_id"]
                )
                income.create()

        return redirect(url_for('get_budget', budget_id=income.budget_id))

    else:
        # if budget item id was specified
        if budget_item_id is not None:
            # grab the budget item from the database
            income = budget_item.query.get(budget_item_id)
            form = BudgetItemForm(obj=income)

        return render_template('_income.html', form=form)

@app.route('/expense', methods=['GET', 'POST'])
def expense():
    # get optional arguments
    budget_id = request.args.get('budget_id')
    budget_item_id = request.args.get('budget_item_id')

    # grab the id for Income item type
    type_id = get_budget_item_type("Expense")

    form = BudgetItemForm(request.form)

    if budget_id is not None: 
        form.budget_id.data = budget_id
    if budget_item_id is not None: 
        form.budget_item_id.data = budget_item_id

    form.budget_item_type_id.data = type_id

    if request.method == 'POST':
        if form.is_submitted():
            if request.form["budget_item_id"] is not None and not request.form["budget_item_id"] == "":
                expense = budget_item.query.get(request.form["budget_item_id"])
                form.populate_obj(expense)
                expense.update()

            else:
                # create income budget item and insert into db
                expense = budget_item(
                    budget_item_type_id = type_id,
                    budget_id = request.form["budget_id"],
                    due_date = request.form["due_date"] if request.form["due_date"] != '' else None,
                    name = request.form["name"],
                    description = request.form["description"],
                    projected_amount = request.form["projected_amount"],
                    fixed = True if request.form.get('fixed', 'n') == 'y' else False
                    #category_id = request.form["category_id"],
                    #sub_category_id = request.form["sub_category_id"]
                )
                expense.create()

        return redirect(url_for('get_budget', budget_id=expense.budget_id))

    else:
        # if budget item id was specified
        if budget_item_id is not None:
            # grab the budget item from the database
            expense = budget_item.query.get(budget_item_id)
            form = BudgetItemForm(obj=expense)

        return render_template('_expense.html', form=form)
    
@app.route('/budget_item/delete/<budget_item_id>', methods=['POST'])
def delete_budget_item(budget_item_id):
    if budget_item_id is not None:
        itm = budget_item.query.get(budget_item_id)
        itm.delete()

    return redirect(url_for('get_budget', budget_id=itm.budget_id))

#endregion

# CONFIGURATION
#region

@app.route('/configuration', methods=['GET'])
@login_required
def configuration():
    
    # renders the dashboard
    return render_template(
        'configuration.html',
        title='Configuration'
    )

#endregion

# HELP
#region

@app.route('/help', methods=['GET'])
def help():
    # render the help page
    return render_template(
        'help.html',
        title='Help'
    )

#endregion

# TEMPLATE FILTERS
#region

@app.template_filter()
def account_balance_format(value):
    value = float(value)
    # negative values denotes income
    return "${:,.2f}".format(value)

@app.template_filter()
def transaction_amount_format(value):
    value = float(value)
    # negative values denotes income
    if value < 0:
        return "+ ${:,.2f}".format(abs(value))
    else:
        return "- ${:,.2f}".format(value) 
    
@app.template_filter()
def income_amount_format(value):
    value = float(value)
    # negative values denotes income
    return "${:,.2f}".format(abs(value))

@app.template_filter()
def transaction_date_format(value):
    date = datetime.strptime(str(value), '%Y-%m-%d')
    return date.strftime('%m.%d')

#endregion

# HELPERS
#region 

# given a string 'type' attempt to find it in db, if it does not exist create it
# return the ID of that type
def get_budget_item_type(type):

    curr = budget_item_type.query.filter_by(name=type).first()

    if curr is None:
        # if the type wasn't found, create it
        curr = budget_item_type(
            name = type,
            active = 1
        )
        curr.create()

    return curr.budget_item_type_id

#endregion