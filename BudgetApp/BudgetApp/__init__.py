"""
The flask application package.
"""

from flask import Flask, session
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = '82u309hgiurbwjbe21h2u3912u30123'

bootstrap = Bootstrap5(app)

import BudgetApp.views
import BudgetApp.plaid
import BudgetApp.models
