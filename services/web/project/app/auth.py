from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import flash
from flask_login.utils import login_user
from project.app.forms import LoginForm
from project.app.models import User

auth = Blueprint('auth', __name__)


# @auth.route('/login')
# def login():
#     return render_template("login.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Username and password are not match! Please try again',
                  category='danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    return "<h1>You have logged out</h1>"


@auth.route('/signup')
def signup():
    return render_template("signup.html")
