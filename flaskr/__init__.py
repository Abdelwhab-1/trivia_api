import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import and_
import random
from werkzeug.exceptions import HTTPException
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def headers(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def categories():
        try:
            all_categories = Category.query.all()
            cats = {}
            for cat in all_categories:
                cats[cat.id] = cat.type
        except Exception as e :
            abort(500)
        return jsonify({
            'categories': cats,
            'success': True
        })
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():
        page_num = int(request.args.get('page',1))

        categories = dict()
        try:
            raw_questions = Question.query.all()
            raw_categories = Category.query.all()
            for category in raw_categories:
                categories[category.id] = category.type
            questions = [question.format() for question in raw_questions]
        except Exception as e :
            abort(500)
        total_questions = len(questions)
        if (page_num - 1) * 10 >= total_questions:
            abort(404)
        try:
            questions = questions[(page_num-1)*10:page_num*10]
        except:
            abort(404)
        current_category = None
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': total_questions,
            'categories': categories,
            'currentCategory': current_category
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete(id):
        question = Question.query.get(id)
        if not question:
            abort(404)
        try:
            question.delete()
        except Exception as e:
            abort(500)

        return jsonify({'success': True})
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def add():
        data = request.get_json()
        for k,v in data.items():
            if v == None:
                abort(400)
        if int(data['category']) not in [id for (id,) in Category.query.with_entities(Category.id).all()]\
                or 0 >= data['difficulty'] > 5:
            abort(422)
        question = Question(question=data['question'], answer=data['answer'], category=data['category'],
                            difficulty=data['difficulty'])
        try:
            question.insert()
        except Exception as e:
            db.session.rollback()
            abort(500)
        return jsonify({
            'success': True,
            'question': question.format(),
            'categories': question.category}), 201
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/search', methods=['POST'])
    def search():
        data = request.get_json()
        query = data['searchTerm']
        raw_questions = Question.query.filter(Question.question.ilike(f'%{query}%')).all()
        questions = [question.format() for question in raw_questions]
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': None
        })
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:id>/questions')
    def get_by_category(id):
        category = Category.query.filter_by(id=id).first()
        if category == None :
            abort(404)
        raw_questions = Question.query.filter_by(category=str(id))
        questions = [question.format() for question in raw_questions]
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': category.format()
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def quizz():
        data = request.get_json()
        categories_id = [ category.id for category in Category.query.all()]
        id = int(data['quiz_category']['id'])
        if id not in categories_id:
            abort(422)
        previous = data['previous_questions']
        future_questions = Question.query.filter(Question.category == str(id)).all()
        next_question = None
        for question in future_questions :
            if question.id not in previous:
                next_question = question.format()
                break

        else:
            abort(404)
        return jsonify({
            'question': next_question,
            'success': True

        })

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            "success": False,
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    return app
if __name__ == "__main__":
    create_app()
