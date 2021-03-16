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
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.question = {
            'question':'what is the module used in testing here new? ',
            'answer': 'unittest',
            'category':1,
            'difficulty': 1
            }
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
    def test_category(self):
        res = self.client.get('/categories')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['categories'])

    def test_get_questions(self):
        res = self.client.get('/questions?page=2')
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['totalQuestions'])
        self.assertIsNotNone(data['categories'])

    def test_get_questions_404(self):
        res = self.client.get('/questions?page=10')
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])

    def test_good_add(self):
        res = self.client.post('/questions', json=self.question)
        data = res.get_json()
        question = Question.query.get(data['question']['id'])
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertDictContainsSubset(self.question, data['question'])
        self.assertEqual(self.question['category'], data['categories'])
        self.assertEqual(question.id, data['question']['id'])


    def test_bad_add_400(self):
        bad_question = self.question
        bad_question['question'] = 'test?'
        bad_question['answer'] = None
        res = self.client.post('/questions', json=bad_question)
        data = res.get_json()
        is_inserted = Question.query.filter(Question.question == self.question['question']).all()
        self.assertEqual(res.status_code,400)
        self.assertEqual(is_inserted,[])
        self.assertEqual(data['code'], 400)


    def test_bad_add_422(self):
        bad_question = self.question
        bad_question['difficulty'] = 6
        bad_question['category'] = 100
        bad_question['question'] = 'test?'
        res = self.client.post('/questions', json=bad_question)
        data = res.get_json()
        self.assertEqual(res.status_code,422)
        self.assertFalse(data['success'])
        self.assertEqual(data['code'], 422)


    def test_search(self):
        res = self.client.post('/search', json={'searchTerm': 'what'})
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue('success')
        self.assertIsNotNone(data['questions'])
        self.assertGreater(data['totalQuestions'],0)


    def test_search_empty(self):
        res = self.client.post('/search', json={'searchTerm': 'من'})
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue('success')
        self.assertListEqual(data['questions'],[])
        self.assertEqual(data['totalQuestions'],0)


    def test_get_by_category(self):
        res = self.client.get('/categories/5/questions')
        data = res.get_json()
        questions = [question.format() for question in Question.query.filter(Question.category=='5').all()]
        category = Category.query.get(5)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertListEqual(questions,data['questions'])
        self.assertDictEqual(category.format(),data['currentCategory'])
        self.assertEqual(len(questions),data['totalQuestions'])


    def test_get_by_category_404(self):
        res = self.client.get('/categories/3847293/questions')
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['code'],404)


    def test_quizz(self):
        res = self.client.post('/quizzes', json={'previous_questions': [5], 'quiz_category': {'id':4} })
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertNotEqual(5, data['question']['id'])


    def test_quizz_422(self):
        res = self.client.post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id':43456345} })
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['code'], 422)


    def test_quizz_404(self):
        res = self.client.post('/quizzes', json={'previous_questions': [5,9,12,23], 'quiz_category': {'id':4} })
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['code'],404)


    def test_delete(self):

        res = self.client.delete('/questions/42')
        data = res.get_json()
        question = Question.query.get(30)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code,200)
        self.assertIsNone(question)


    def test_delete_404(self):
        res = self.client.delete('/questions/3756767868969790')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()