# BudgetApp

This repository was created to aid in the version control for our Software Engineering Capstone Project.

## Getting Started

### Prerequisites

- Python 3.10 
- Visual Studio

### Installation for Development

To get this project running, it requires some initial setup

1. First, a local MySQL server instance must be installed and running on the localhost of the development machine.

    - To do this, download the <a href="https://dev.mysql.com/downloads/">MySQL Installer</a> and install both MySQL Server and MySQL Workbench.

    - Use <a href="https://ladvien.com/data-analytics-mysql-localhost-setup/">this quide</a> to get it started.

2. Next, it is necessary to create a mock database that will be used for testing since it is impractical and insecure for it to point at the production database hosted on Namecheap.

    - To do this, open the localhost MySQL server on MySQL Workbench and create a new schema named 'finance'.

    - Next, open a new query tab and run the table creation scripts located in the db_init.sql file in the repo's root directory.

    - In the future, I will create a python script to automate this process but for now the scripts must be run manually.

3. Next, verify that Python 3.10 is installed on your machine.

	- If it is not, go to <a href="https://www.python.org/downloads/">Python downloads page</a> and install the most recent version of Python 3.10
	
	- You might need to update the Python executable location in the configs
	
		- To do this, make sure you have python installed then press WIN key and search for Python ...
		- Find Python 3.10, right click and Open File Location
		- Find the Shortcut for Python 3.10, right click and select Properties
		- Copy the Target Directory
		- Next, in the solution in Visual Studio find BudgetApp > BudgetApp > env > pyvenv.cfg > open this file with a text editor
		- Change the home directory to be the Target directory you copied earlier (make sure to remove the python.exe from the end)

4. Next, open the Solution in Visual Studio (will not work in visual studio code)

	- Next, find BudgetApp > BudgetApp > Python Environments
	
	- Create a new environment using Python 3.10
	
	- Make sure to install packages from requirements.txt
	
		- Right click on the new environment you created and click 'Install from requirements.txt'
	
5. Once you have the necessary packages installed, open the DbContext class 

	- You can find this in BudgetApp > BudgetApp > BudgetApp > models > DbContext.py
	
	- Find the 'SQLALCHEMY_DATABASE_URI' connection string.

	- Change the Username and Password to reflect that of the user you created in the steps above.
	
	- You should not need to change anything else since the port should default to 3306 and your db name should be 'finance'
	
6. Finally, you should be good to run the project 

## Contribution Instructions

- NOTES:

	- Make sure if you install any additional packages to update the requirements.txt file.
		- You can do this by right clicking your Python Environment > Generate requirements.txt > Update and add entries

	- <a href="https://endjin.com/blog/2020/07/debugging-web-apps-in-visual-studio-with-custom-browser-configurations">Change browser that Visual Studio runs web project in </a>
	
## Authors

- Jack Grantham
- Joshua Brander
- Srinivas Harini Akula

## Acknowledgements

- <a href="https://www.nintyzeros.com/2019/11/flask-mysql-crud-restful-api.html">Help with Flask/SqlAlchemy Integration</a>