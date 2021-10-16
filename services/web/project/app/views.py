from flask import Blueprint, render_template
from flask.helpers import send_from_directory
from flask_login import login_required, current_user
from project.app.models import *

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/questions')
@login_required
def questions():
	# Create a list of questions.
	questions = Question.query.order_by(Question.date_created).all()
	# For each question add the username of the creator, and the number of answers as attributes.
	for q in questions:
		q.creator = User.query.get(q.userId)
		q.numAnswers = len(Answer.query.filter_by(questionId = Answer.questionId).all())
	return render_template("questions.html", user=current_user, questions_list=questions)

# Temporary method returns files in static/css/
@views.route('/static/css/<filename>')
def staticfile(filename):
	return send_from_directory('app/static/css/', filename)

# BUG: The function below does not return the files in static as expected.
# @views.route("/static/<path:filename>")
# def staticfile(filename):
#     return send_from_directory(views.config["STATIC_FOLDER"], filename)
