from flask_login import current_user
from project import db
from project.app.models import User, Question, Answer
from project.app.forms import NewAnswerForm


class QuestionCtrl():

    def getQuestion(question_id):
        result = list()
        # Get question from DB
        question = Question.query.get(question_id)

        # Validate that question exists; if not, route to questions forum
        if question is None:
            result.append('ERROR')
            result.append('QUESTION_DOES_NOT_EXIST')
            return result

        # Get list of answers for question
        question.answers = Answer.query.filter_by(
            questionId=question.id).order_by(Answer.numVotes.desc()).all()
        question.numAnswers = len(question.answers)
        # Default value, condition is checked below
        question.hasAcceptedAnswer = False
        # Default value, condition is checked below
        question.user_is_owner = False
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
        if (current_user.is_authenticated):
            if(current_user.id == question.userId):
                question.user_is_owner = True

        # Process form
        form = NewAnswerForm()
        if form.validate_on_submit():
            body = form.body.data
            # Add answer to DB
            a = Answer(body, current_user.id, question.id)
            db.session.add(a)
            db.session.commit()

            result.append("SUCCESS")
            result.append("NEW_ANSWER_CREATED")
            result.append(question_id)
            return result

        # For each answer, add the creator as an attribute
        for a in question.answers:
            a.creator = User.query.get(a.userId)

        result.append("SUCCESS")
        result.append("QUESTION_FOUND")
        result.append(question)
        result.append(form)
        return result

    def acceptAnswer(answer_id, question_id):
        result = list()
        # Get all answers for question; filter by is_accepted_answer = true
        accepted_answer = Answer.query.filter_by(
            is_accepted_answer=True, questionId=question_id).all()
        # If question does not yet have a best answer then
        if(len(accepted_answer) < 1):
            # Get answer from DB
            answer = Answer.query.get(answer_id)
            #  If answer could not be found
            if(answer is None):
                # Return error message to user
                # TODO: Log error to file instead.
                result.append("ERROR")
                result.append("ANSWER_NOT_FOUND_ERROR")
                return result

            # TODO: If user is not owner of question, log error.

            # Otherwise update is_accepted_answer column of answer to true
            answer.is_accepted_answer = True
            db.session.commit()
            # Reload question so that accepted answer
            # appears at top of the list.
            result.append("SUCCESS")
            result.append("views.question")
            result.append("getQuestion")
            result.append(question_id)
            return result
        # If question already has a best answer the
        else:
            # Return error message to user
            # TODO: Log error to file instead.
            result.append("ERROR")
            result.append("ACCEPTED_ANSWER_EXISTS")
            return result


class UserCtrl():
    def getUser(user_id):
        result = list()
        # get user from DB
        user = User.query.get(user_id)

        # validate that user exists
        if user is None:
            result.append("ERROR")
            result.append("USER_DOES_NOT_EXIST")
            return result

        # get all questions posted by user
        questions = Question.query.filter_by(
            userId=user.id).order_by(Question.numVotes.desc()).all()
        # get num of questions asked
        questions.numQuestions = len(questions)

        # send back the result object with all information
        result.append("SUCCESS")
        result.append("USER_FOUND")
        result.append(user)
        result.append(questions)
        return result
