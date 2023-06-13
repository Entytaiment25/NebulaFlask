import logging
import os
import re

import asgiref.wsgi
from argon2 import PasswordHasher
from dotenv import load_dotenv
from flask import Flask, escape, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

load_dotenv()

env = os.getenv


## Generate a random secret key
def generate_secret_key():
    if env("SECRET_KEY") is None or env("SECRET_KEY") == "":
        return os.urandom(24).hex()


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = env("DB_URI")  # Update the key name here
app.config["SECRET_KEY"] = generate_secret_key()
app.config["SESSION_COOKIE_SECURE"] = env("SESSION_COOKIE_SECURE")
app.config["SESSION_COOKIE_HTTPONLY"] = env("SESSION_COOKIE_HTTPONLY")
app.config["SESSION_COOKIE_SAMESITE"] = env("SESSION_COOKIE_SAMESITE")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = env("SQLALCHEMY_TRACK_MODIFICATIONS")

db = SQLAlchemy(app)
ph = PasswordHasher()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")

        ## Validate input
        if not username or not password or not name:
            return render_template(
                "register.html", error="Please provide a username, password, and name."
            )

        ## Check if the username already exists
        if Users.query.filter_by(username=username).first() is not None:
            return render_template("register.html", error="Username already exists.")

        ## Password validation
        if not is_valid_password(password):
            return render_template(
                "register.html",
                error="Password must be at least 8 characters long and contain at least 1 special character and 1 number.",
            )

        ## Hash the password
        password_hash = ph.hash(password)

        ## Create a new user
        new_user = Users(username=username, password_hash=password_hash, name=name)
        db.session.add(new_user)
        db.session.commit()

        logging.getLogger().info(f"New user registered: {username}")

        return redirect(url_for("login"))

    return render_template("register.html")


def is_valid_password(password):
    ## Password must be at least 8 characters long and contain at least 1 special character and 1 number
    regex = r"^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$"
    return re.match(regex, password) is not None


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        ## Retrieve the user from the database using parameterized query
        user = (
            Users.query.filter(text("username = :username"))
            .params(username=username)
            .first()
        )

        if not user:
            return render_template("login.html", error="Invalid username or password.")

        ## Verify the password
        try:
            ph.verify(user.password_hash, password)
        except:
            return render_template("login.html", error="Invalid username or password.")

        ## Store the user's session
        session["username"] = user.username

        logging.getLogger().info(f"User logged in: {user.username}")

        return redirect(url_for("dashboard", username=user.username))

    return render_template("login.html")


@app.route("/dashboard/<username>")
def dashboard(username):
    ## Check if the user is authenticated
    if session.get("username") != username:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=username)


app = asgiref.wsgi.WsgiToAsgi(app)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import uvicorn

    uvicorn.run(app, host=env("HOST_IP"), port=int(env("HOST_PORT")))
