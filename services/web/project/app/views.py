from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import send_from_directory
from flask_login import login_required, current_user
from project import app, db
from project.app.models import User, Question, Answer
from project.app.forms import NewQuestionForm, NewAnswerForm

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
        q.numAnswers = len(Answer.query.filter_by(questionId=q.id).all())
    return render_template("questions.html", user=current_user, questions_list=questions)


@views.route('/question', methods=['GET', 'POST'])
@login_required
def new_question():
    form = NewQuestionForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        # Add new question in DB
        q = Question(title, body, current_user.id)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for("views.question", question_id=q.id))

    return render_template("new_question.html", form=form)


@views.route('/questions/<question_id>', methods=['GET', 'POST'])
def question(question_id):
    # Get question from DB
    question = Question.query.get(question_id)
    # Validate that question exists; if not, route to questions forum
    if question == None:
        questions()
        questions()
        questions()
    # Get list of answers for question
    question.answers = Answer.query.filter_by(questionId=question.id).all()
    question.numAnswers = len(question.answers)
    # Get the question's creator and assign it as an attribute
    question.creator = User.query.get(question.userId)

    # Process form
    form = NewAnswerForm()
    if form.validate_on_submit():
        body = form.body.data
        # Add answer to DB
        a = Answer(body, current_user.id, question.id)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('views.question', question_id=question_id))

    # For each answer, add the creator as an attribute
    for a in question.answers:
        a.creator = User.query.get(a.userId)
    return render_template('question.html', question=question, form=form)

# BUG: The function below does not return the files in static as expected.
# @views.route("/static/<path:filename>")
# def static_file(filename):
#     return send_from_directory(app.config["STATIC_FOLDER"], filename)


# Temporary method returns files in static/css/
@views.route('/static/css/<filename>')
def staticfile(filename):
    return send_from_directory('app/static/css/', filename)
