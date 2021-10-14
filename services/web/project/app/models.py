from flask_login.mixins import UserMixin
from project.extensions import db, login_manager
from project.helpers import models
import bcrypt



@login_manager.user_loader
def user_loader(user):
    return User.query.get(user)


class User(models.BaseModel, UserMixin):
    __tablename__ = "users"

    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

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
        self.password_hash = bcrypt.hashpw(
            plain_text_password.encode('ascii'), bcrypt.gensalt())

    def check_password_correction(self, attempted_password):
        return bcrypt.checkpw(self.password, attempted_password)
