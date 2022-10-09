# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.


## Error Handling
Errors are returned as JSON onjects in the format below:
```
{
  'success': False,
  'error: 400,
  'message': Request Not Acceptable
}
```

The API will return three error types when requests fail:
- 400: Request Not Acceptable
- 404: No Resource Found
- 422: Unprocessable
- 500: Internal Server Error

## Endpoints

### GET /categories
-General
  - Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs, a key: value pair of `success: True` and the number of categories available `total_categories: 6`.
  - Request Arguments: None

-Sample: `curl -X GET http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

### GET /questions
- General 
  - Returns a list of questions, total questions, object including all categories and current category string
  - Ensured the questions are paginated, with only 10 questions appearing per page
  - Request Arguments: 

- Sample: `curl -X GET http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```

### DELETE /questions/<int:question_id>
- General
  - Deletes a specific question using the id of the question
  - Request Argument: `question_id` which is an integer
  - Returns a `success: True` to indicate success at deleting a question from the database

-Sample: `curl -X DELETE http://127.0.0.1:5000/questions/24 -H "Content-Type: application/json"`

```
{
  "success": true
}
```

### POST /questions
- General 
  - Create a new question 
  - Request Body: 
    ```
    {
      'question': 'Here's a new question string',
      'answer': 'Here's the answer to the question',
      'difficulty': '2',
      'category': 4
    }
    ```
  - Returns a json object with `success: True` key, value pair to indicate success in inserting a new object into the database

- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"question\": \"What is the meaning of Chinonyelum?\", \"answer\": \"God is mine\", \"category\": 2, \"difficulty\": 4}"`
- Response
  ```
  {
  "success": true
  }
  ```

### POST /questions
- General
  - Gets questions based on a search term - any phrase
  - Request Body: 
    ```
    {
      "searchTerm": "first"
    }
    ```
  - Returns a json object which contains a `success: True` key value pair, an array of the questions object that contain the search term, count of questions, and the current category

- Sample : `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\": \"first\"}" http://127.0.0.1:5000/questions`
- Response
  ```
  {
  "currentCategory": "Sports",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
  }
  ```

### GET /categories/<int:category_id>/questions

- General
  - Gets questions based on category
  - Request Argument: `category_id` which is an integer
  - Returns an object containing the questions that are in the category indicated, the total amount of questions found in the category and the current category

- Sample: 
- Response Body:
  ```
  {
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "God is mine",
      "category": 2,
      "difficulty": 4,
      "id": 26,
      "question": "What is the meaning of Chinonyelum?"
    }
  ],
  "success": true,
  "total_questions": 5
  }
  ```

### POST /quizzes
- General 
  - Gets the questions to play the quiz
  - Request Body:
    {
      'previous_questions': '[1, 4, 8, 5, 19]',
      'quiz_category': 'this is one of the quiz categories'
    }
  - Returns a `question` object which differs if/not a category is selected
- Sample:
  _Without category specified_ 
  `curl -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": \"[1, 4, 8, 21]\"}" http://127.0.0.1:5000/quizzes`
  
  _With category specified_
  `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21],"quiz_category": {"type": "Science", "id": "1"}}'`

  
- Response 
  _Without category specified_
  ```
  {
  "question": {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  "success": true
  }
  ```
  _With category specified_
  ```
  {
  "question": {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true

  ```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
