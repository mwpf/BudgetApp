import mysql.connector
from pymysql import NULL

# handle connection and CRUD functionality to the database
class FinanceDbContext:

    # default constructor
    def __init__(self):
        
        # connect to local MySQL database on localhost
        self.finance = mysql.connector.connect(
            host = "localhost",
            port = '3306',
            user = "sa",
            password = "rhgJeNBQBG$99",
            db = 'finance'
        )

# end FinanceDbContext