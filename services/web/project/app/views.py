from flask import Blueprint, render_template, redirect, url_for, request
from flask.helpers import send_file

from flask_login import login_required, current_user
from project import db
from project.app.models import User, Question, Answer
from project.app.forms import NewAnswerForm, NewQuestionForm
from project.app.controllers import QuestionCtrl

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return questions()


@views.route('/questions')
def questions():
    # Create a list of questions.
    questions = Question.query.order_by(Question.numVotes.desc()).all()
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
            question_id=q.id))

    return render_template("new_question.html", form=form)


@views.route('/questions/<question_id>', methods=['GET'])
def question(question_id):
    question = QuestionCtrl.getQuestion(question_id)

    return render_template("question.html", question=question, form=NewAnswerForm())


@login_required
@views.route('/questions/<question_id>', methods=['POST'])
def newAnswer(question_id):
    '''Post request for a new answer'''
    QuestionCtrl.newAnswer(question_id)
    return redirect(url_for("views.question", question_id))


@login_required
@views.route('/questions/accept_answer/<a_id>/<q_id>', methods=['GET'])
def acceptAnswer(a_id, q_id):
    '''Accept Answer'''
    # The controller returns the following in the result list:
    # - the status of the operation (result[0]) : "SUCCESSS" | "ERROR"
    # - the error message following a status of "ERROR" (result[1])
    result = QuestionCtrl.acceptAnswer(a_id, q_id)
    # if operation was performed successfully
    if(result[0] == "SUCCESS"):
        # Reload the question to load changes in accepted answer
        return redirect(url_for(
            "views.question",
            question_id=q_id))
    # else result[0] = "ERROR"
    else:
        error_message = result[1]
        return error_message


@login_required
@views.route('/vote/<question_id>/<answer_id>/<value>', methods=['GET'])
def vote(question_id, answer_id, value):
    '''Up/downvote an asnwer'''
    answer_to_update = Answer.query.get(answer_id)
    # num_votes_by_user = User.query.get(current_user.id).dailyVotes

    # if(num_votes_by_user >= 10):
    #     flash('You have exceded 10 votes for the day. You will be allowed to
    # vote again tomorrow at 6:30 am. Thank you',
    #           category='error')
    #     return redirect(request.referrer)
    # elif(num_votes_by_user < 10):

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


@login_required
@views.route('/questionVote/<question_id>/<value>', methods=['GET'])
def questionVote(question_id, value):
    '''Up/downvote a question'''
    question_to_update = Question.query.get(question_id)
    # num_votes_by_user = User.query.get(current_user.id).dailyVotes

    # if(num_votes_by_user >= 10):
    #     flash('You have exceeded 10 votes for the day. You will be allowed to
    # vote again tomorrow at 6:30 am. Thank you',
    #           category='error')
    #     return redirect(request.referrer)
    # elif(num_votes_by_user < 10):

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


# Temporary method returns files in static/*/
@views.route('/static/<folder>/<filename>')
def staticfile(folder, filename):
    path = 'app/static/' + folder + '/' + filename
    return send_file(path)
