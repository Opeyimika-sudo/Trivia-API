import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from random import randint
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. 
    Delete the sample route after completing the TODOs
    """
    # CORS(app, resources ={r"/api/": {"origins": "*"}})
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,DELETE,POST,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()

            if len(categories) == 0:
                abort(404)

            else: 
                return jsonify({
                    'success': True,
                    'categories': {
                        category.id: category.type for category in categories
                    },
                    'total_categories': len({category.id: category.type for category in categories})
                })

        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_all_questions_with_pagination():
        page = request.args.get('page', 1, type=int) 
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        try:
            questions = Question.query.all()

            formatted_questions = [question.format() for question in questions]

            categories = Category.query.all()

            questions_array = formatted_questions[start:end]
            if len(formatted_questions[start:end]) == 0:
                abort(404)

            else: 
                return jsonify({
                    'success': True,
                    'questions': formatted_questions[start:end],
                    'categories': {category.id:category.type for category in categories},
                    'total_questions': len(Question.query.all()),
                    'current_category': Category.query.filter(Category.id == questions_array[len(questions_array) - 1]['category']).one_or_none().type
                })

        except:
            abort(404)
            

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        try:
            if question is None:
                abort(404)

            else:
                question.delete()

                return jsonify({
                    'success': True,
                    'deleted': question_id

                })
            
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_new_or_search_for_question():
        body = request.get_json()
        if len(body) == 0:
                    abort(404)
        else:
            try:
                if 'searchTerm' in body:
                    searchTerm = body['searchTerm']
                    questions = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()

                    if len(questions) == 0:
                        abort(404)

                    else:
                        formatted_questions = [question.format() for question in questions]

                        for question in questions:
                            category = question.category
                            currentCategory = Category.query.filter(Category.id == category).one_or_none().type


                        return jsonify({
                            'success': True,
                            'questions': formatted_questions,
                            'total_questions': len(formatted_questions),
                            'currentCategory': currentCategory
                        })
                    

                else:
                        newQuestion = body['question']
                        newAnswer = body['answer']
                        newDifficulty = body['difficulty']
                        newCategory = body['category']

                        question = Question(question=newQuestion, answer=newAnswer, difficulty=newDifficulty, category=newCategory)

                        question.insert()

                        return jsonify({
                            'success': True
                        })

            except:
                abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=["GET"])
    def get_questions_based_on_category(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id).all()

            if len(questions) == 0:
                abort(404)

            else:
                formatted_questions = [question.format() for question in questions]

                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': Category.query.filter(Category.id == category_id).one_or_none().type
                })
        except:
            abort(404)

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
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')
        category_id = category['id']


        if category_id == 0:
            questions = Question.query.order_by(func.random())
        else:
            questions = Question.query.filter(
            Question.category == category_id).order_by(func.random())

    
        question = questions.filter(Question.id.notin_(
            previous_questions)).first()
        if question is None:
            return jsonify({
                'success': True
            })
    
        return jsonify({
            'success': True,
            'question': question.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({
            'success': False,
            'status_code': 404,
            'message': 'no resource found'
        }), 404

    @app.errorhandler(422)
    def request_not_processed(error):
        return jsonify({
            'success': False,
            'status_code': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': 'request not acceptable'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'status_code': 500,
            'message': 'internal server error'
        }), 500

    return app