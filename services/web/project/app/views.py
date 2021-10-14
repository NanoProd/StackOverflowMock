from flask import Blueprint, render_template
from flask.helpers import send_from_directory
from flask_login.utils import login_required

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html")


@views.route("/static/<path:filename>")
def staticfile(filename):
    return send_from_directory(views.config["STATIC_FOLDER"], filename)
