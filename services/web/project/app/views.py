from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import send_from_directory, flash
from flask_login import login_required, current_user
from project.app.models import *
from project.app.forms import NewQuestionForm

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return questions()

@views.route('/questions')
def questions():
	# Create a list of questions.
	questions = Question.query.order_by(Question.date_created).all()
	# For each question add the username of the creator, and the number of answers as attributes.
	for q in questions:
		q.creator = User.query.get(q.userId)
		q.numAnswers = len(Answer.query.filter_by(questionId = Answer.questionId).all())
	return render_template("questions.html", user=current_user, questions_list=questions)

@views.route('/new_question', methods=['GET','POST'])
@login_required
def new_question():
	form = NewQuestionForm()
	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data
		# Add new question in DB
		q = Question(title,body,current_user.id)
		db.session.add(q)
		db.session.commit()
		return question(q)

	return render_template("new_question.html", form=form)

@views.route('/question')
@login_required
def question(question):
	return question.title

# Temporary method returns files in static/css/
@views.route('/static/css/<filename>')
def staticfile(filename):
	return send_from_directory('app/static/css/', filename)

# BUG: The function below does not return the files in static as expected.
# @views.route("/static/<path:filename>")
# def staticfile(filename):
#     return send_from_directory(views.config["STATIC_FOLDER"], filename)
