# Mortgage Loan Calculator
#### Video Demo:  https://www.youtube.com/watch?v=Xqc5pNZj7Nk
#### Description:

This project is a Loan Calculator web application built using Flask, a Python web framework. It allows users to calculate loan details based on various parameters such as purchase price, down payment, interest rate, loan type, and more. Users can also register, log in, and view their loan history.

# How to run:

## Run in Docker 

Clone the project  

~~~bash  
  git clone https://github.com/jomacaag/LoanCalc
~~~

Go to the project directory  

~~~bash  
  cd PPW
~~~

Initialize dependencies in pyhton vitrual enviroment  

~~~bash  
pip install virtualenv
virtualenv venv
source venve/bin/activate
pip install -r requirements.txt
~~~

Initialize databases
~~~bash
flask initdb
~~~

Start the server  

~~~bash  
flask run
~~~


# Explanation

## Files

- `app.py`: This is the main Python file that contains the Flask application code. It handles routing, request handling, and database interactions.
- `loancalc.db`: This file is an SQLite database file that stores user and loan data. It is created and initialized by the `initdb` command.
- `README.md`: This file provides an overview of the project, its functionality, and the purpose of each file.

## Design Choices

### Flask Configuration

The Flask application is configured with the following settings:
- Secret key: A randomly generated secret key is used to secure the session data and protect against cross-site scripting attacks.
- Session type: The session data is stored on the file system.
- Database URI: An SQLite database file is used for storing user and loan data.
- SQLAlchemy track modifications: This setting is disabled to improve performance.

### Database Models

The application uses SQLAlchemy to define two database models:
- `users`: This model represents user data and includes fields for the user ID, username, and password hash.
- `Loan`: This model represents loan data and includes fields for various loan parameters such as purchase price, interest rate, down payment, loan type, and more.

### Routes and Views

The Flask application defines the following routes:
- `/`: This is the root route that renders the index.html template, which contains the main page of the application.
- `/calculated`: This route handles loan calculation. It retrieves the input values from the request, performs the necessary calculations, and renders the calculated.html template with the results.
- `/history`: This route allows logged-in users to view their loan history. It retrieves the loan data from the database and renders it in the history.html template.
- `/login`: This route handles user login. It verifies the login credentials and sets the user ID in the session.
- `/register`: This route handles user registration. It validates the input data, creates a new user in the database, and logs in the user.
- `/logout`: This route logs the user out by clearing the session.


### Commands

The application includes a custom Flask command called `initdb`. When executed, this command drops and recreates the database, initializing it with the required tables.

## Conclusion

This Loan Calculator web application provides users with a convenient way to calculate loan details based on various parameters. It also includes user registration, login, and loan history functionality. The project utilizes Flask, SQLAlchemy, and SQLite to handle the web application's backend operations.


