USE finance;

CREATE TABLE IF NOT EXISTS user
(
	user_id INT NOT NULL,
	email VARCHAR(255) NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_user PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS plaid_item
(
	item_id VARCHAR(255) NOT NULL,
	user_id INT NOT NULL,
	institution_id VARCHAR(255),
	webhook VARCHAR(255),
	request_id VARCHAR(255) NOT NULL,
	access_token VARCHAR(255) NOT NULL,
	created_by VARCHAR(255) NOT NULL,
	created_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_plaid_item PRIMARY KEY (item_id),
	CONSTRAINT fk_plaid_item_user FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS account
(
	account_id VARCHAR(255) NOT NULL,
	item_id VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	official_name VARCHAR(255) NOT NULL,
	available_balance DECIMAL NOT NULL,
	current_balance DECIMAL NOT NULL,
	`limit` VARCHAR(255) NULL,
	iso_currency_code VARCHAR(255) NOT NULL,
	last_updated_date_time DATETIME NOT NULL,
	mask VARCHAR(255) NOT NULL,
	type VARCHAR(255) NOT NULL,
	sub_type VARCHAR(255) NOT NULL,
	verification_status VARCHAR(255) NULL,
	request_id VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_account PRIMARY KEY (account_id),
	CONSTRAINT fk_account_plaid_item FOREIGN KEY (item_id) REFERENCES plaid_item(item_id)
);

CREATE TABLE IF NOT EXISTS category
(
	category_id INT NOT NULL,
	name VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_category PRIMARY KEY (category_id)
);

CREATE TABLE IF NOT EXISTS budget
(
	budget_id INT NOT NULL,
	user_id INT NOT NULL,
	month VARCHAR(10) NOT NULL,
	year VARCHAR(4) NOT NULL,
	created_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT pk_budget PRIMARY KEY (budget_id),
	CONSTRAINT fk_budget_user FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS budget_item_type
(
	budget_item_type_id INT NOT NULL,
	name VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_budget_item_type PRIMARY KEY (budget_item_type_id)
);

CREATE TABLE IF NOT EXISTS budget_item
(
	budget_item_id INT NOT NULL,
	budget_item_type_id INT NOT NULL,
	budget_id INT NOT NULL,
	fixed BOOLEAN NOT NULL,
	due_date DATE NOT NULL,
	name VARCHAR(255) NOT NULL,
	description VARCHAR(255) NOT NULL,
	projected_amount DECIMAL NOT NULL,
	actual_amount DECIMAL NOT NULL,
	category_id INT NOT NULL,
	sub_category_id INT NOT NULL,
	CONSTRAINT pk_budget_item PRIMARY KEY (budget_item_id),
    CONSTRAINT fk_budget_item_budget FOREIGN KEY (budget_id) REFERENCES budget (budget_id),
	CONSTRAINT fk_budget_item_budget_item_type FOREIGN KEY (budget_item_type_id) REFERENCES budget_item_type (budget_item_type_id),
	CONSTRAINT fk_budget_item_category FOREIGN KEY (category_id) REFERENCES category (category_id),
    CONSTRAINT fk_budget_item_subcategory FOREIGN KEY (sub_category_id) REFERENCES category (category_id)
);

CREATE TABLE IF NOT EXISTS transaction
(
	transaction_id VARCHAR(255) NOT NULL,
	account_id VARCHAR(255) NOT NULL,
	amount DECIMAL NULL,
	iso_currency_code VARCHAR(255) NULL,
    category_id VARCHAR(255) NULL,
    store_number VARCHAR(255) NULL,
    payer VARCHAR(255) NULL,
	payee VARCHAR(255) NULL,
    reference_number VARCHAR(255) NULL,
	by_order_of VARCHAR(255) NULL,
	payment_method VARCHAR(255) NULL,
	payment_processor VARCHAR(255) NULL,
    reason VARCHAR(255) NULL,
	account_owner VARCHAR(255) NULL,
	name VARCHAR(255) NULL,
	original_description VARCHAR(255) NULL,
	date DATE NULL,
	pending BOOLEAN NULL,
	merchant_name VARCHAR(255) NULL,
	check_number VARCHAR(255) NULL,
	payment_channel VARCHAR(255) NULL,
	transaction_code VARCHAR(255) NULL,
	transaction_type VARCHAR(255) NULL,
	CONSTRAINT pk_transaction PRIMARY KEY (transaction_id),
	CONSTRAINT fk_transaction_account FOREIGN KEY (account_id) REFERENCES account (account_id)
);

CREATE TABLE IF NOT EXISTS transaction_type
(
	transaction_type_id INT NOT NULL,
	name VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_transaction_type PRIMARY KEY (transaction_type_id)
);

CREATE TABLE IF NOT EXISTS transaction_detail
(
	transaction_detail_id INT NOT NULL,
	transaction_id VARCHAR(255) NOT NULL,
	transaction_type_id INT NOT NULL,
	budget_item_id INT NOT NULL,		
	custom_description VARCHAR(255) NOT NULL,
	CONSTRAINT pk_transaction_detail PRIMARY KEY (transaction_detail_id),
	CONSTRAINT fk_transaction_detail_transaction FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id),
	CONSTRAINT fk_transaction_detail_transaction_type FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(transaction_type_id),
	CONSTRAINT fk_transaction_detail_budget_item FOREIGN KEY (budget_item_id) REFERENCES budget_item(budget_item_id)
);

CREATE TABLE IF NOT EXISTS location
(
	location_id INT NOT NULL,
	transaction_id VARCHAR(255) NOT NULL,
	address VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
	region VARCHAR(255) NOT NULL,
	postal_code VARCHAR(255) NOT NULL,
	country VARCHAR(255) NOT NULL,
	latitude DECIMAL NOT NULL,
	longitude DECIMAL NOT NULL,
	store_number VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL,
	CONSTRAINT pk_location PRIMARY KEY (location_id)
);