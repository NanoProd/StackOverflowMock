from flask.cli import FlaskGroup
from flask_sqlalchemy import model
from project import app
from project.extensions import db
from project.app.models import *


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(username="test", email="johnas@concordia.ca", password="test"))
    db.session.add(Question(title="Test Question", body="This is a test question. It is intended to be inserted into the DB as a seed.", userId=1))
    db.session.add(Answer(body="This is a test answer. It is intended to be inserted into the DB as a seed.", userId=1, questionId=1))
    db.session.commit()


if __name__ == "__main__":
    cli()
