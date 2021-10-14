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
    db.session.add(User(username="test", email="johnas@concordia.ca",
                        password="test"))
    db.session.commit()


if __name__ == "__main__":
    cli()
