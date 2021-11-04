from flask import Blueprint, render_template, redirect, url_for, request
from flask.helpers import flash, send_from_directory

from flask_login import login_required, current_user
from project import db
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
    if question is None:
        questions()
    # Get list of answers for question
    question.answers = Answer.query.filter_by(
        questionId=question.id).order_by(Answer.numVotes.desc()).all()
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
        return redirect(url_for('views.question', question_id=question_id, user=current_user))

    # For each answer, add the creator as an attribute
    for a in question.answers:
        a.creator = User.query.get(a.userId)
    return render_template('question.html', question=question, form=form, user=current_user)


@views.route('/vote/<question_id>/<answer_id>/<value>', methods=['GET'])
def vote(question_id, answer_id, value):
    answer_to_update = Answer.query.get(answer_id)
    num_votes_by_user = User.query.get(current_user.id).dailyVotes

    if(num_votes_by_user >= 10):
        flash('You have exceded 10 votes for the day. You will be allowed to vote again tomorrow at 6:30 am. Thank you',
              category='error')
        return redirect(request.referrer)
    elif(num_votes_by_user < 10):
        # increase votes of user in db
        voter = User.query.get(current_user.id)
        voter.dailyVotes += 1
        db.session.commit()
        if int(value) == 1:
            answer_to_update.numVotes += 1
        else:
            answer_to_update.numVotes -= 1
        try:
            db.session.commit()
        except Exception:
            return "There was a problem updating votes"
    return redirect(request.referrer)


@views.route('/questionVote/<question_id>/<value>', methods=['GET'])
def questionVote(question_id, value):
    question_to_update = Question.query.get(question_id)
    num_votes_by_user = User.query.get(current_user.id).dailyVotes

    if(num_votes_by_user >= 10):
        flash('You have exceeded 10 votes for the day. You will be allowed to vote again tomorrow at 6:30 am. Thank you', category='error')
        return redirect(request.referrer)
    elif(num_votes_by_user < 10):
        # increase votes of user in db
        voter = User.query.get(current_user.id)
        voter.dailyVotes += 1
        db.session.commit()
        if int(value) == 1:
            question_to_update.numVotes += 1
        else:
            question_to_update -= 1
        try:
            db.session.commit()
        except Exception:
            return "There was a problem updating votes"
    return redirect(request.referrer)


# Temporary method returns files in static/css/


@views.route('/static/css/<filename>')
def staticfile(filename):
    return send_from_directory('app/static/css/', filename)
# BUG: The function below does not return the files in static as expected.
# @views.route("/static/<path:filename>")
# def staticfile(filename):
#     return send_from_directory(views.config["STATIC_FOLDER"], filename)
