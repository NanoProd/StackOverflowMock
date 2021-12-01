# service/web/tests/test_base.py

import os
import unittest


from project.main import app
from project.extensions import db
from project.app.models import Answer, Question, User


class BasicTest(unittest.TestCase):
    _test_db_path = os.path.join(app.config['BASEDIR'], 'test.db')

    # setup and teardown

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'Just some giberish for testing purposes'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            self._test_db_path

        with app.app_context():
            db.drop_all()
            db.create_all()

        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        os.unlink(self._test_db_path)

    def seedTestData(self):
        with app.app_context():
            db.session.add(
                User(username="test", email="johnas@concordia.ca", password="test"))
            db.session.add(Question(title="Test Question 1",
                                    body="This is a test question. It is intended to be inserted into the DB as a seed.", userId=1))
            db.session.add(Answer(
                body="#1 This is a test answer. It is intended to be inserted into the DB as a seed.", userId=1, questionId=1))
            db.session.add(Answer(
                body="#2 This is a test answer. It is intended to be inserted into the DB as a seed.", userId=1, questionId=1))
            db.session.add(Question(title="Test Question 2",
                                    body="This is a test question. It is intended to be inserted into the DB as a seed.", userId=1))
            db.session.add(Answer(
                body="#1 This is a test answer. It is intended to be inserted into the DB as a seed.", userId=1, questionId=2))
            db.session.add(Answer(
                body="#2 This is a test answer. It is intended to be inserted into the DB as a seed.", userId=1, questionId=2))
            db.session.commit()


if __name__ == "__main__":
    unittest.main()
