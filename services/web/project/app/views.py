from flask import Blueprint, render_template, redirect, url_for, request
from flask.helpers import send_file

from flask_login import login_required, current_user
from project import db
from project.app.models import User, Question, Answer
from project.app.forms import NewAnswerForm, NewQuestionForm
from project.app.controllers import QuestionCtrl
from project.app.controllers import UserCtrl

views = Blueprint('views', __name__)


@views.route('/')
def home():
    '''Just a homepage'''
    questions = Question.query.order_by(Question.numVotes.desc()).all()
    for q in questions:
        q.creator = User.query.get(q.userId)
        q.numAnswers = len(Answer.query.filter_by(questionId=q.id).all())
    return render_template('questions.html', questions_list=questions)


@views.route('/questions')
def questions():
    '''List of all questions'''
    questions = Question.query.order_by(Question.numVotes.desc()).all()
    # For each question add the username of the creator,
    # and the number of answers as attributes.
    for q in questions:
        q.creator = User.query.get(q.userId)
        q.numAnswers = len(Answer.query.filter_by(questionId=q.id).all())
    return render_template(
        "questions.html", user=current_user, questions_list=questions
    )


@views.route('/question', methods=['GET', 'POST'])
@login_required
def newQuestion():
    '''Show new question form and post it to database'''
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


@views.route('/questions/<question_id>', methods=['GET'])
def showQuestion(question_id):
    '''Show question by its id'''
    question = QuestionCtrl.getQuestion(question_id)

    return render_template(
        "question.html", question=question, form=NewAnswerForm()
    )


@views.route('/questions/<question_id>', methods=['POST'])
@login_required
def newAnswer(question_id):
    '''Post request for a new answer'''
    QuestionCtrl.newAnswer(question_id)
    return redirect(url_for("views.question", question_id))


@views.route('/questions/accept_answer/<a_id>/<q_id>', methods=['GET'])
@login_required
def acceptAnswer(a_id, q_id):
    '''Accept Answer'''
    # The controller returns the following in the result list:
    # - the status of the operation (result[0]) : "SUCCESSS" | "ERROR"
    # - the error message following a status of "ERROR" (result[1])
    result = QuestionCtrl.acceptAnswer(a_id, q_id)
    # if operation was performed successfully
    if(result[0] == "SUCCESS"):
        # Reload the question to load changes in accepted answer

        # increase reputation of user who posted the question
        post_user_id = Question.query.get(q_id).userId
        post_user = User.query.get(post_user_id)

        if current_user.id != post_user.id:
            post_user.reputation += 15
            # increase reputation of user who accepted the answer
            current_user.reputation += 2

        return redirect(url_for("views.question", question_id=q_id))
    # else result[0] = "ERROR"
    else:
        error_message = result[1]
        return error_message


@views.route('/vote/<question_id>/<answer_id>/<value>', methods=['GET'])
@login_required
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

    # get user who posted the question
    post_user_id = Question.query.get(question_id).userId
    post_user = User.query.get(post_user_id)

    # increase votes of user in db
    voter = User.query.get(current_user.id)
    voter.dailyVotes += 1
    db.session.commit()
    if int(value) == 1:
        post_user.reputation += 10
        answer_to_update.numVotes += 1
    else:
        answer_to_update.numVotes -= 1
    try:
        db.session.commit()
    except Exception:
        return "There was a problem updating votes"

    return redirect(request.referrer)


@views.route('/questionVote/<question_id>/<value>', methods=['GET'])
@login_required
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

    # get user who posted the question
    post_user_id = Question.query.get(question_id).userId
    post_user = User.query.get(post_user_id)

    # increase votes of user in db
    voter = User.query.get(current_user.id)
    voter.dailyVotes += 1
    db.session.commit()
    if int(value) == 1:
        post_user.reputation += 10
        question_to_update.numVotes += 1
    else:
        question_to_update -= 1
    try:
        db.session.commit()
    except Exception:
        return "There was a problem updating votes"

    return redirect(request.referrer)


@views.route('/userPage/<user_id>', methods=['GET', 'POST'])
def userPage(user_id):
    result = UserCtrl.getUser(user_id)
    # The controller returns the results as a list:
    # result[0] : Operation Status => value = "SUCCESS" | "ERROR"
    # result[1] : Message => value "succes_or_error_message"
    # result[2] : User object
    #   associated with result[0] = "SUCCESS" and result[1] = "USER_FOUND"
    # result[3] : Questions object
    #   associated wit result[0] = "SUCCESS" and result[1] = "USER_FOUND"

    # if operation was a success
    if(result[0] == "SUCCESS"):
        message = result[1]
        if(message == "USER_FOUND"):
            _user = result[2]
            _questions = result[3]
            for q in _questions:
                q.creator = User.query.get(q.userId)
                q.numAnswers = len(
                    Answer.query.filter_by(questionId=q.id).all())
            return render_template("userPage.html",
                                   user=_user, questions=_questions)
    else:
        # Redirect to home
        return redirect(url_for("home.html"))


@views.route('/static/<folder>/<filename>')
def staticfile(folder, filename):
    '''Technical route for retrieving static files in static/*/'''
    path = 'app/static/' + folder + '/' + filename
    return send_file(path)
