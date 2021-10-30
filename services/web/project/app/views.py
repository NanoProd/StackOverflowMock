from flask import Blueprint, render_template, redirect, url_for, request
from flask.helpers import send_file

from flask_login import login_required, current_user
from project import db
from project.app.models import User, Question, Answer
from project.app.forms import NewQuestionForm
from project.app.controllers import QuestionCtrl

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return questions()


@views.route('/questions')
def questions():
    # Create a list of questions.
    questions = Question.query.order_by(Question.date_created).all()
    # For each question add the username of the creator,
    # and the number of answers as attributes.
    for q in questions:
        q.creator = User.query.get(q.userId)
        q.numAnswers = len(Answer.query.filter_by(questionId=q.id).all())
    return render_template(
        "questions.html",
        user=current_user,
        questions_list=questions)


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
        return redirect(url_for(
            "views.question",
            method="getQuestion",
            arg1=q.id))

    return render_template("new_question.html", form=form)


@views.route('/questions/', defaults={
    'method': 'None',
    'arg1': 'None',
    'arg2': 'None'})
@views.route('/questions/<method>/', defaults={
    'arg1': 'None',
    'arg2': 'None'})
@views.route('/questions/<method>/<arg1>', defaults={
    'arg2': 'None'},
    methods=['GET', 'POST'])
@views.route('/questions/<method>/<arg1>/<arg2>', methods=['GET', 'POST'])
def question(method, arg1, arg2):
    # Make best answer method
    if(method == "acceptAnswer"):
        result = QuestionCtrl.acceptAnswer(arg1, arg2)
        if(result[0] == "REDIRECT"):
            return redirect(url_for(
                result[1],
                method=result[2],
                arg1=result[3]))
        else:
            return result
    # Get Queston method
    elif(method == "getQuestion"):
        result = QuestionCtrl.getQuestion(arg1)
        if(result[0] == "REDIRECT_1"):
            return redirect(url_for(result[1]))
        elif(result[0] == "REDIRECT_2"):
            return redirect(url_for(
                result[1],
                method=result[2],
                arg1=result[3]))
        else:
            return render_template(
                result[1],
                question=result[2],
                form=result[3])
    else:
        return redirect(url_for("views.questions"))


@views.route('/vote/<question_id>/<answer_id>/<value>', methods=['GET'])
def vote(question_id, answer_id, value):
    answer_to_update = Answer.query.get(answer_id)
    if int(value) == 1:
        answer_to_update.numVotes += 1
    else:
        answer_to_update.numVotes -= 1
    try:
        db.session.commit()
    except Exception:
        return "There was a problem updating votes"
    return redirect(request.referrer)


# Temporary method returns files in static/*/
@views.route('/static/<folder>/<filename>')
def staticfile(folder, filename):
    path = 'app/static/' + folder + '/' + filename
    return send_file(path)
