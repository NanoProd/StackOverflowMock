from project.extensions import db, login_manager
from project.helpers import models


@login_manager.user_loader
def user_loader(user):
    return User.get(user)


class User(models.BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
