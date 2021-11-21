from flask import Flask, request, Response, json
from utils import extract_field_from_body
import database

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


@app.route('/quizzes/<id>', methods=['GET'])
def get_quiz(id):

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        user_id = extract_field_from_body('user_id', body)

        quiz = database.get_quiz(db_connection, id, user_id)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps(quiz), status=200, mimetype='application/json')


@app.route('/quizzes/short_url/<short_url>', methods=['GET'])
def get_quiz_by_short_url(short_url):
    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        user_id = extract_field_from_body('user_id', body)

        id = database.get_quiz_id(db_connection, short_url)

        quiz = database.get_quiz(db_connection, id, user_id)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps(quiz), status=200, mimetype='application/json')


@app.route('/quizzes/<quiz_id>/answer', methods=['POST'])
def answer_quiz(quiz_id):
    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        user_id = extract_field_from_body('user_id', body)
        option_id = extract_field_from_body('option_id', body)

        database.answer(db_connection, quiz_id, user_id, option_id)

        database.result(db_connection, quiz_id)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response('Answer added.', status=201, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
