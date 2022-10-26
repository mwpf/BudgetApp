# BudgetApp

This repository was created to aid in the version control for our Software Engineering Capstone Project.



## Getting Started

### Prerequisites

- NPM & NodeJS
- Python 3 

### Installation

To get this project running, it requires some initial setup

1. First, a local MySQL server instance must be installed and running on the localhost of the development machine.

    - To do this, download the <a href="https://dev.mysql.com/downloads/">MySQL Installer</a> and install both MySQL Server and MySQL Workbench.

    - Use <a href="https://ladvien.com/data-analytics-mysql-localhost-setup/">this quide</a> to get it started.

2. Next, it is necessary to create a mock database that will be used for testing since it is impractical and insecure for it to point at the production database hosted on Namecheap.

    - To do this, open the localhost MySQL server on MySQL Workbench and create a new schema named 'finance'.

    - Next, open a new query tab and run the table creation scripts located in the db_init.sql file in the repo's root directory.

    - In the future, I will create a python script to automate this process but for now the scripts must be run manually.

3. Finally, we can attempt to run the project.

    - To do this, open the project in VS Code and in a new terminal type the following commands:
    
    <br />
    
    ```sh
    cd python
    ```

    - If running for the first time:

    <br />

    ```sh
    pip3 install -r requirements.txt
    ```

    - Next (you can skip to this command if not running for the first time):

    <br />

    ```sh
    ./start.sh
    ```

    - This should start the backend of the project.
    - To start the frontend, open a new terminal window and type the following commands:

    <br />
    
    ```sh
    cd frontend
    ```

    - If running for the first time:

    <br />
    
    ```sh
    npm install
    ```

    ```sh
    npm ci --force
    ```

    - Next (you can skip to this command if not running for the first time):

    <br />

    ```sh
    npm start
    ```

    - This should open a new tab in your default browser containing a running version of the project.

## Usage

- 

## Authors

- Jack Grantham
- Joshua Brander
- Srinivas Harini Akula

## Acknowledgements

- <a href=""></a>