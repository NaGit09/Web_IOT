from flask import Blueprint, render_template

web_bp = Blueprint("web_bp", __name__)


@web_bp.route("/")
def home():
    return render_template("index.html")

@web_bp.route("/login")
def login():
    return render_template("login.html")

@web_bp.route("/history")
def history():
    return render_template("history.html")
