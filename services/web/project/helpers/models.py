from project.extensions import db
from sqlalchemy.sql import func


class BaseModel(db.Model):
    """
    Abstract model
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now())
