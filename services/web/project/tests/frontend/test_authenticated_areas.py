# service/web/tests/front_end/authenticated_areas.py
import unittest
from project.tests.test_base import BasicTest


class AuthenticatedAreas(BasicTest):
    # tests
    def test_ask_question_is_denied_to_a_visitor(self):
        '''Visitor is redirected to auth if tries to ask a new question'''
        response = self.app.get('/question', follow_redirects=False)
        self.assertIn('/login?next=%2Fquestion', response.location)

    def test_log_out_is_denied_to_a_visitor(self):
        '''A visitor is redirected to auth page if tries to log out'''
        response = self.app.get('/logout', follow_redirects=False)
        self.assertIn('/login?next=%2Flogout', response.location)

    def test_a_visitor_cannot_post_answers(self):
        '''A visitor is redirected to auth page if tries to post an answer'''
        response = self.app.post('/logout', follow_redirects=False)
        self.assertIn('/login?next=%2Flogout', response.location)


if __name__ == "__main__":
    unittest.main()
