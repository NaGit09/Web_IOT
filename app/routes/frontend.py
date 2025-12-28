from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
from app.services.api import API

web_bp = Blueprint("web_bp", __name__)


# Login Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("web_bp.login"))
        return f(*args, **kwargs)

    return decorated_function


@web_bp.route("/")
@login_required
def home():
    return render_template("index.html")


@web_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Use API Service to verify login
        if API().login(
            request.get_json().get("username"), request.get_json().get("password")
        ):
            session["user"] = request.get_json().get("username")
            return redirect(url_for("web_bp.home"))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng!", "error")

    return render_template("login.html")


@web_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("web_bp.login"))


@web_bp.route("/history")
@login_required
def history():
    return render_template("history.html")


@web_bp.route("/data")
@login_required
def data():
    return render_template("data.html")


@web_bp.route("/device")
@login_required
def device():
    return render_template("device.html")


@web_bp.route("/contact")
@login_required
def contact():
    return render_template("contact.html")
