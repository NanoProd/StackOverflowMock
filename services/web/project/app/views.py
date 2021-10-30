from flask import Blueprint, render_template, redirect, url_for, request
from flask.helpers import send_file

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
        return redirect(url_for("views.question", method="getQuestion", arg1=q.id))

    return render_template("new_question.html", form=form)


@views.route('/questions/', defaults={'method': 'None', 'arg1': 'None', 'arg2': 'None'})
@views.route('/questions/<method>/', defaults={'arg1': 'None', 'arg2': 'None'})
@views.route('/questions/<method>/<arg1>', defaults={'arg2': 'None'}, methods=['GET', 'POST'])
@views.route('/questions/<method>/<arg1>/<arg2>', methods=['GET', 'POST'])
def question(method, arg1, arg2):
    # Make best answer method
    if(method == "acceptAnswer"):
        answer_id = arg1
        question_id = arg2
        # Get all answers for question; filter by is_accepted_answer = true
        accepted_answer = Answer.query.filter_by(is_accepted_answer=True, questionId=question_id).all()
        # If question does not yet have a best answer then
        if(len(accepted_answer) < 1):
            # Get answer from DB
            answer = Answer.query.get(answer_id)
            #  If answer could not be found
            if(answer is None):
                # Return error message to user
                # TODO: Log error to file instead.
                return "ANSWER_NOT_FOUND_ERROR"

            # TODO: If user is not owner of question, log error.

            # Otherwise update is_accepted_answer column of answer to true
            answer.is_accepted_answer = True
            db.session.commit()
            # Reload question so that accepted answer appears at top of the list.
            return redirect(url_for("views.question", method="getQuestion", arg1=question_id))
        # If question already has a best answer the
        else:
            # Return error message to user
            # TODO: Log error to file instead.
            return "ACCEPTED_ANSWER_EXISTS"
    # Get Queston method
    elif(method == "getQuestion"):
        # Get question from DB
        question = Question.query.get(arg1)
        # Validate that question exists; if not, route to questions forum
        if question is None:
            questions()
        # Get list of answers for question
        question.answers = Answer.query.filter_by(questionId=question.id).order_by(Answer.numVotes.desc()).all()
        question.numAnswers = len(question.answers)
        question.hasAcceptedAnswer = False  # Default value, condition is checked below
        question.user_is_owner = False  # Default value, condition is checked below
        # Get the question's creator and assign it as an attribute
        question.creator = User.query.get(question.userId)

        # Place accepted answer at the top of the list
        for a in question.answers:
            if(a.is_accepted_answer is True):
                # Remove answer from list.
                question.answers.remove(a)
                # Prepend answer to list.
                question.answers.insert(0, a)
                # Indicate that question has accepted answer
                question.hasAcceptedAnswer = True

        # Determine if user owns question
        if (current_user.id == question.userId):
            question.user_is_owner = True

        # Process form
        form = NewAnswerForm()
        if form.validate_on_submit():
            body = form.body.data
            # Add answer to DB
            a = Answer(body, current_user.id, question.id)
            db.session.add(a)
            db.session.commit()
            return redirect(url_for('views.question', method="getQuestion", arg1=question.id))

        # For each answer, add the creator as an attribute
        for a in question.answers:
            a.creator = User.query.get(a.userId)
        return render_template('question.html', question=question, form=form)
    else:
        return questions()


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
