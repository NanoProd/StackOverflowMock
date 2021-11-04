from flask_login.mixins import UserMixin
from project.extensions import db, login_manager
from project.helpers import models
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def user_loader(user):
    return User.query.get(user)


class User(models.BaseModel, UserMixin):
    __tablename__ = "users"

    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    dailyVotes = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, username, email, password):
        self.email = email
        self.password = password
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = generate_password_hash(
            plain_text_password,
            method='sha256'
        )

    def check_password_correction(self, attempted_password):
        return check_password_hash(self.password, attempted_password)


class Question(models.BaseModel):
    __tablename__ = "questions"

    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    numVotes = db.Column(db.Integer, default=0, nullable=False)
    userId = db.Column(db.Integer, nullable=False)

    def __init__(self, title, body, userId):
        self.title = title
        self.body = body
        self.userId = userId

    def __repr__(self):
        return '<Question %r>' % self.title


class Answer(models.BaseModel):
    __tablename__ = "answers"

    body = db.Column(db.String, nullable=False)
    numVotes = db.Column(db.Integer, default=0, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    questionId = db.Column(db.Integer, nullable=False)

    def __init__(self, body, userId, questionId):
        self.body = body
        self.userId = userId
        self.questionId = questionId
