
from email.policy import default
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from BudgetApp import app

"""
RESOURCES:
    https://www.nintyzeros.com/2019/11/flask-mysql-crud-restful-api.html
USAGE:
    
    # GET
    get_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    products = product_schema.dump(get_products)
    return make_response(jsonify({"product": products}))

    # POST
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product": result}),200)

    # PUT
    data = request.get_json()
    get_product = Product.query.get(id)
    if data.get('title'):
        get_product.title = data['title']
    if data.get('productDescription'):
        get_product.productDescription = data['productDescription']
    if data.get('productBrand'):
        get_product.productBrand = data['productBrand']
    if data.get('price'):
        get_product.price= data['price']    
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['id', 'title', 'productDescription','productBrand','price'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))
"""

# Template: 'mysql+pymysql://<mysql_username>:<mysql_password>@<mysql_host>:<mysql_port>/<mysql_db>'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:rhgJeNBQBG$99@localhost:3306/finance'
db = SQLAlchemy(app)

# USER
#region

class user(UserMixin, db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    first_name  = db.Column(db.String(255))
    last_name  = db.Column(db.String(255))
    active  = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class user_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = user
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# PLAID ITEM
#region

class plaid_item(db.Model):
    __tablename__ = "plaid_item"

    item_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    institution_id = db.Column(db.String(255))
    webhook = db.Column(db.String(255))
    request_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    created_by = db.Column(db.String(255))
    created_date_time = db.Column(db.DateTime)
    active  = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class plaid_item_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = plaid_item
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# ACCOUNT
#region

class account(db.Model):
    __tablename__ = "account"

    account_id = db.Column(db.String(255), primary_key=True)
    item_id = db.Column(db.String(255), db.ForeignKey('plaid_item.item_id'))
    name = db.Column(db.String(255))
    official_name = db.Column(db.String(255))
    available_balance = db.Column(db.Float, nullable=True)
    current_balance = db.Column(db.Float)
    limit = db.Column(db.String(255))
    iso_currency_code = db.Column(db.String(255))
    last_updated_date_time = db.Column(db.DateTime)
    mask = db.Column(db.String(255))
    type = db.Column(db.String(255))
    sub_type = db.Column(db.String(255))
    verification_status = db.Column(db.String(255))
    request_id = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class account_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = account
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# CATEGORY
#region

class category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class category_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = category
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# BUDGET
#region

class budget(db.Model):
    __tablename__ = "budget"

    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    month = db.Column(db.String(10))
    year = db.Column(db.String(4))
    created_date_time = db.Column(db.DateTime)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class budget_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = budget
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# BUDGET ITEM TYPE
#region

class budget_item_type(db.Model):
    __tablename__ = "budget_item_type"

    budget_item_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class budget_item_type_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = budget_item_type
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# BUDGET ITEM
#region

class budget_item(db.Model):
    __tablename__ = "budget_item"

    budget_item_id = db.Column(db.Integer, primary_key=True)
    budget_item_type_id = db.Column(db.Integer, db.ForeignKey('budget_item_type.budget_item_type_id'))
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.budget_id'))
    fixed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    projected_amount = db.Column(db.Float)
    actual_amount = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    sub_category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class budget_item_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = budget_item
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# TRANSACTION
#region

class transaction(db.Model):
    __tablename__ = "transaction"

    transaction_id = db.Column(db.Integer, primary_key=True)
    plaid_transaction_id = db.Column(db.String(255))
    account_id = db.Column(db.String(255), db.ForeignKey('account.account_id'))
    amount = db.Column(db.Float)
    iso_currency_code = db.Column(db.String(255))
    category_id = db.Column(db.String(255))
    store_number = db.Column(db.String(255))
    payer = db.Column(db.String(255))
    payee = db.Column(db.String(255))
    reference_number = db.Column(db.String(255))
    by_order_of = db.Column(db.String(255))
    payment_method = db.Column(db.String(255))
    payment_processor = db.Column(db.String(255))
    reason = db.Column(db.String(255))
    account_owner = db.Column(db.String(255))
    name = db.Column(db.String(255))
    original_description = db.Column(db.String(255))
    date = db.Column(db.Date)
    pending = db.Column(db.Boolean)
    merchant_name = db.Column(db.String(255))
    check_number = db.Column(db.String(255))
    payment_channel = db.Column(db.String(255))
    transaction_code = db.Column(db.String(255))
    transaction_type = db.Column(db.String(255))

    def __getitem__(self, field):
        return self.__dict__[field]
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class transaction_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = transaction
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# TRANSACTION TYPE
#region

class transaction_type(db.Model):
    __tablename__ = "transaction_type"

    transaction_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class transaction_type_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = transaction_type
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# TRANSACTION DETAIL
#region

class transaction_detail(db.Model):
    __tablename__ = "transaction_detail"

    transaction_detail_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.transaction_id'))
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('transaction_type.transaction_type_id'))
    budget_item_id = db.Column(db.Integer, db.ForeignKey('budget_item.budget_item_id'))		
    custom_description = db.Column(db.String(255))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class transaction_detail_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = transaction_detail
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion

# LOCATION
#region

class location(db.Model):
    __tablename__ = "location"

    location_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    region = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    country = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    store_number = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return

class location_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = location
        include_relationships = True
        load_instance = True
        sqla_session = db.session

#endregion
