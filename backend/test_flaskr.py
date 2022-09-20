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
        self.database_name = "trivia"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.postQuestion = {"id": "29","question":"Next Nigeria president?", "answer":"Peter Obi", "difficulty":"1","category":"5"}

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
    
    # def test_categories(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['total_categories'], 6)
    #     self.assertTrue(data['categories'])

    # def test_categories_404(self):
    #     res = self.client().get('/categories/1')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'],False)
    #     self.assertEqual(data['message'], 'resource not found')
    #     self.assertEqual(res.status_code, 404)

    # def test_questions(self):
    #     res = self.client().get("/questions", json={'page': 1})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertEqual(data['current_category'], 'ALL')
    #     self.assertTrue(data['categories'])

    # def test_question_valid_page(self):
    #     res = self.client().get("/questions?page=6000")
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #     self.assertEqual(res.status_code, 404)

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/25")
    #     print(res.data)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])

    # def test_questions_search(self):
    #     res = self.client().post("/questions/search", json={"searchTerm":"What"})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])

    # def test_question_add(self):
    #     res = self.client().post("/questions", json=self.postQuestion)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)

    # def test_question_add_failure(self):
    #     res = self.client().post("/questions/5", json=self.postQuestion)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['message'], 'method not allowed')
    #     self.assertEqual(data['success'],False)

    # def test_questions_search_without_result(self):
    #     res = self.client().post("/questions/search", json={"searchTerm":"some questions that doesn't exist"})
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200) 
    #     self.assertEqual(len(data['questions']), 0)
    #     self.assertEqual(data['total_questions'], 0)

    # def test_random_question_by_category(self):
    #     res = self.client().post("/quiz", json={"previous_questions": [], "quiz_category":{"type":"Science", "id":"1"}})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])
        

    def test_random_question_by_category_failure(self):
        res = self.client().post("/quiz", json={"previous_questions": [], "quiz_category":{"type":"Science", "id":"12"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)
        
    # def test_delete_question_failure(self):
    #     res = self.client().delete("/questions/20001")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()