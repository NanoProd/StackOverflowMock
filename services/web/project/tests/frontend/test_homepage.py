# service/web/tests/front_end/test_homepage.py
import unittest
from project.tests.test_base import BasicTest


class HomePageTest(BasicTest):
    # tests
    def test_homepage_status_code_200(self):
        '''Home page is sending 200'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_visitor_can_see_default_test_seed_questions(self):
        '''A visitor can see default test questions'''
        self.seedTestData()
        response = self.app.get('/')
        self.assertIn(b'Test Question 1', response.data)
        # self.assertIn(b'1 Votes', response.data)
        # self.assertIn(b'2 Answers', response.data)
        self.assertIn(b'Asked by:', response.data)
        self.assertIn(
            b'This is a test question. It is intended to be inserted into the DB as a seed.', response.data)
        self.assertIn(b'Test Question 2', response.data)

    def test_visitor_can_see_naviation_buttons(self):
        '''A visitor can see navigation buttons'''
        response = self.app.get('/')
        self.assertIn(b'Login', response.data, 'Login button is present')
        self.assertIn(b'Sign-up', response.data, 'Sign-up button is present')
        self.assertIn(b'Log out', response.data, 'Log out button is present')
        self.assertIn(b'Questions', response.data,
                      'Questions button is present')

    def test_visitor_can_see_ask_questions_button(self):
        '''A visitor can see ask question button'''
        response = self.app.get('/')
        self.assertIn(b'Ask Question', response.data)


if __name__ == "__main__":
    unittest.main()
