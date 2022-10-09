import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res=self.client().get('/categories')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_404_unable_to_get_categories(self):
        res= self.client().get('/categories/1')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'no resource found')

    def test_get_all_questions_with_pagination(self):
        res = self.client().get('/questions?page=1')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_unable_to_access_page_not_in_db(self):
        res=self.client().get('/questions?page=1000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'no resource found')

    def test_delete_question(self):
        res=self.client().delete('/questions/19')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 19).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)
       
    def test_422_unable_to_delete_question(self):
        res = self.client().delete('/questions/400')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        res=self.client().post('/questions', json = {
            'question': "What is the name of Aremu Opeyimika's lover?",
            'answer': "Chinonyelum",
            'difficulty': 5,
            'category': 4
        })
        data= json.loads(res.data)

        question = Question.query.filter(Question.answer == "Chinonyelum").one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(question)

    def test_400_unable_to_create_new_question(self):
        res=self.client().post('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not acceptable')

    def test_post_search_item(self):
        res = self.client().post('/questions', json={
        'searchTerm': 'first'
    })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_unable_to_retrieve_search_item(self):
        res= self.client().post('/questions', json={
            'searchTerm': 'jkjdkfkdk'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'no resource found')

    def test_get_questions_based_on_category(self):
        res= self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_404_unable_to_get_questions_based_on_category(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'no resource found')

    def test_start_quiz(self):
        res = self.client().post("/quizzes", 
        json = {
            "previous_questions": [1, 4, 8, 9],
            "quiz_category": {'type': 'Science', 'id': 1}
            }
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_fail_to_start_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not acceptable')
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()