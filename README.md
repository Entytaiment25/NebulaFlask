# NebulaFlask

## Secure Flask User Registration and Login witg Argon2 Password Hashing and MySQL Database Storage

This is a Flask application that provides user registration and login functionality. It uses the Argon2 password hashing algorithm for secure password storage. The application uses SQLAlchemy as the ORM (Object-Relational Mapping) tool to interact with a MySQL database.

## Features

- User registration: Users can create a new account by providing a unique username, password, and name.
- User login: Registered users can log in to access their dashboard.
- Password validation: Passwords must be at least 8 characters long and contain at least 1 special character and 1 number.
- Session management: User sessions are stored using Flask's session management, allowing authenticated access to protected routes.
- Logging: The application logs new user registrations and successful user logins.

## Usage

**1.** Install the required dependencies listed in the "Dependencies" section.

```bash
pip install flask flask_sqlalchemy argon2-cffi mysqlclient uvicorn gunicorn gevent asgiref python-dotenv
```

or

```bash
pip install -r requirements.txt
```

**2.** Set up a MySQL database and update the "SQLALCHEMY_DATABASE_URI" configuration in the code to point to your database.

- I used XAMPP to set up a local MySQL database for testing and imported the users.sql file to create the user table.

**3.** Run the application.

```bash
uvicorn main:app
```

**4.** Access the application in your web browser and register a new user.

**5.** Log in with the registered user's credentials and access the user's dashboard.

Note: This code is provided as a basic example and may need further enhancements and security considerations for production use. Make sure to properly secure your application and database when deploying it.

## Dependencies

- Python 3.6+ (I used Python 3.11.3)

## Attention

- this was tested with Windows 11 Pro 22H2 22621.1778
- for Unix systems, you may need to change some things

## Found a bug?

Feel free to open a new issue. Make sure to include as much information as possible so I can reproduce the bug or open a pull request.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
