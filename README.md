# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



# Trivia
## _RestAPI For a guessing game_



Trivia is a RESTAPI game for testing your knowledge. it was  built using python `flask`. It uses the convintional http methods to detairmen how to manipulate the data. 
#### Base URL 
```
http://127.0.0.1:5000/ 
```
#### Authentication 
this API doesn't require any Authentication 

## Errors 
these are the errors you may encounter while you use the API. The API uses `HTTP conventional Status Codes`.

- 404 Not found 
    - the resource you are trying to access doesn't exist
- 500 Internal error
    - something went wrong with the server. 
- 422 Unprocessable Entity
    - you interred a valid inputs syntactically, but it doesn't make sense for example you chose a category that doesn't exist for your question. 
- 400 Bad Request
    - you have interred wrong syntax for example interring integer instead of a string. 
### Error response body 
```
{
    "success": False,
    "code": code,
    "name": name,
    "description": descrepiton  
    
}
```
### Example
```
{
    "success": False,
    "code": 404,
    "name": Not Found,
    "description": "The requested URL was not found on the server. 
                    If you entered the URL manually please check 
                    your spelling and try again.",
}
```
## Access Points 

``` GET /categories ```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a 2 keys, categories, that contains a object of id: category_string key:value pairs and success, a blean that have value ture to indicate that it was  successful request. 


##### Example 

```
GET /categories
response =  {
            'success': True,
            'categories': {'1':'scince','2':'history'},
            }
```
``` GET /categories/category_id/questions ```
- Fetches a dictionary of question that belong to one category
- Request Arguments: None
- Returns: An object with a 4 keys,  `totalQuestions` which is the total number of questions in that category, `currentCategory` which is the dictionary of the category requested caontain id,type keys and their values , `questions` which is a list contains questions which is a dictionary that have id, question, category, and answer keys all representing the question data, and finally `success` which is bolean have the value true indicating that every thing went well.    


##### Example 

```
GET /categories/1/questions
response =  {
            'success': True,
            'questions': [   {
                                id:1,
                                question: 'what is Trivia?',
                                category: '1',       
                                answer: 'RestAPI'
                            }
                        ],
            'totalQuestions': 1,        # this is the number of the total amount of questions that's available
            'currentCategory':  1,
            }
```
``` GET /questions?page=page_number ```
- Fetches a dictionary of question that have 10 questions varieng depending on the number of the page.
- Request Arguments: None
- Returns: An object with a 5 keys,  `totalQuestions` which is the total number of questions in the database, `categories` which is the dictionary of all categories id,type keys and their values , `questions` which is a list contains questions which is a dictionary that have id, question, category, and answer keys all representing the question data, `currentCategory` which is allows None, and finally `success` which is bolean have the value true indicating that every thing went well.  
    
##### Example 
```
GET /questions?page=5
response =  {
            success: True,
            questions: [{
                            id:1,
                            question: 'what is Trivia?',
                            category: '1',       
                            answer: 'RestAPI'}],
            totalQuestions: 1, # this is the number of the total amount of questions that's available
            categories: {1:'test'},
            currentCategory: None
            }
```
``` DELETE /questions/question_id ```
- Delete the question with the id in the URI 
- Request Arguments: None
- Returns: object that have 1 key `success` indicating that the request was successful
##### Example 
```
DELETE /questions/1
response =  {success: True}
```

``` POST /questions ```
- Adds new question. 
- Request Arguments: boject that have `question`,`answer`,`difficulty`,`category` representing the data of question 
- Returns: An object with a 3 keys, `Category` which is the id of the new question's category, `question` which is and object that have id, question, category, and answer keys all representing the question data, and finally `success` which is bolean have the value true indicating that every thing went well.    
##### Example 
```
POST /questions
data = {
        question: 'the question',
        answer: 'the answer',
        difficulty: 1,
        category: 1
      }
```
Response 
```
{
    question:   {id:1,
                question: 'what is Trivia?',
                category: '1',       
                answer: 'RestAPI'},
    category:   1,
    success:    True,
}
```


``` POST /quizzes ```
- Fetches a dictionary that have 1 question only.
- Request Arguments: object that have one key `searchTerm`
- Returns: An object with a 2 keys,   `questions` which is an option  that is a dictionary that have `id`, `question`, `category`, and `answer` keys all representing the question data, and socend key `success` which is bolean have the value true indicating that every thing went well. 

##### Example 
```
POST /questions
data = {
        previous_questions: [2],
        quiz_category: {'id':1},
      }
```
Response 
```
{
    question:   {id:1,
                question: 'what is Trivia?',
                category: '1',       
                answer: 'RestAPI'},
    success:    True,
}
```
``` POST /search ```
- Fetches a dictionary of questions that have the search term in thier body.
- Request Arguments: object that have one key `searchTerm`
- Returns: An object with a 4 keys,  `totalQuestions` which is the total number of questions in the database,  `questions` which is a list contains questions that is a dictionary that have `id`, `question`, `category`, and `answer` keys all representing the question data, `currentCategory` which is allows None, and finally `success` which is bolean have the value true indicating that every thing went well. 

##### Example 
```
POST /search
data = {{searchTerm: searchTerm}: 'what'}
```
Response 
```
{
    questions:   [{id:1,
                question: 'what is Trivia?',
                category: '1',       
                answer: 'RestAPI'}],
    success:    True,
    currentCategory: None
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```