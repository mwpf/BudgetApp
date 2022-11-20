"""
The flask application package.
"""

from flask import Flask
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

bootstrap = Bootstrap5(app)

import BudgetApp.views
import BudgetApp.plaid
import BudgetApp.models
