from time import sleep
from flask import (
    Blueprint,
    get_flashed_messages,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, User


auth = Blueprint("auth", __name__)
api_auth = HTTPBasicAuth()


@api_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if user and check_password_hash(user.password, password):
        return username


@auth.get("/login")
def login_page():
    return render_template("login.html")


@auth.post("/me")
@api_auth.login_required
def get_me():
    return api_auth.current_user()


@auth.post("/login")
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=bool(remember))
    return redirect(url_for("main.profile"))


@auth.get("/signup")
def register_page():
    return render_template("signup.html")


@auth.post("/signup")
def register():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        flash("User already exists.")
        print(get_flashed_messages())
        sleep(3)
        return redirect(url_for("auth.login"))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
