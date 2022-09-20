import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    formattedQuestion = questions[start:end]

    return formattedQuestion


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """ @TODO: Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        formattedCat = [category.format()['type'] for category in categories]

        return jsonify({
            'success': True,
            'categories': formattedCat,
            'total_categories': len(formattedCat)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()

        formattedQuestion = paginate_questions(request, questions)

        categories = Category.query.order_by(Category.id).all()

        formattedCat = [category.format()['type'] for category in categories]
        initial_category = "ALL"

        if len(formattedQuestion) < 1:
            abort(404)
        return jsonify({
            'success': True,
            'questions': formattedQuestion,
            'current_category': initial_category,
            'categories': formattedCat,
            'total_questions': len(questions)
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database
    and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            question.delete()
            total_questions = Question.query.all()
            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(total_questions)
            })
        except BaseException:

            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            staging_question = Question(
                question=question, answer=answer,
                category=category,
                difficulty=difficulty
            )
            staging_question.insert()

            return jsonify({
                "success": True,
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def search_questions():
        body = request.get_json()
        search_query = body.get('searchTerm', None).lower()
        print(search_query)
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_query))).all()
        formattedQuestions = [question.format() for question in questions]
        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'current_category': 'ALL',
            'questions': formattedQuestions,
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        current_category = Category.query.filter(Category.id == category_id + 1).one_or_none()

        if (current_category is None):
            abort(404)
        try:
            questions = Question.query.filter(Question.category == category_id + 1).all()
            formattedQuestions = [question.format() for question in questions]

            return jsonify({
                'questions': formattedQuestions,
                'total_questions': len(formattedQuestions),
                'current_category': current_category.format(),
            })
        except BaseException:
            abort((404))

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quiz', methods=['POST'])
    def play_the_game():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")
            if (quiz_category == 0 or quiz_category['id'] == 0):
                questions = Question.query.all()
                formattedQuestions =[question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'question': formattedQuestions[random.randint(0, len(formattedQuestions) - 1)]
                })
            else:
                questions = Question.query.filter(Question.category == quiz_category['id']).all()

                formattedQuestions = [question.format() for question in questions]

                for single_question in formattedQuestions:
                    while single_question['id'] not in previous_questions:

                        return jsonify({
                            'success': True,
                            'question': single_question
                        })
            return jsonify({
                'success': True,
                'question': None
            })
        except BaseException:
            abort(404)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "request cannot be processed"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "An internl server error occured"
        }), 500
    return app
