from flask import Blueprint, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from extensions import bcrypt, db_session
from services import UserService

userService = UserService()

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = userService.get_user_by_email(db_session(), username.data)
        if existing_user_username:
            print(existing_user_username)
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


@auth_bp.route("/login")
def login():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        user = userService.get_user_by_email(db_session(), username)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect("/home")
        else:
            print(
                f"Invalid user or {user.password} {bcrypt.generate_password_hash(password)}",
                "error",
            )
    else:
        print(f"{request.method} invalid form submission! {form.errors}")

    return redirect("/")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return render_template("logout.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            userService.create_user(db_session(), username, password)
            return redirect(url_for("auth.login"))
        else:
            print(f"{request.method} invalid form submission! {form.errors}")

    return render_template("register.html")