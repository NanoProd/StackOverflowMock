from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<h1>You have logged out</h1>"


@auth.route('/signup')
def signup():
    return render_template("signup.html")
