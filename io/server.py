from flask import Flask, request, Response, json
from utils import extract_field_from_body
import database

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


@app.route('/users', methods=['POST'])
def create_user():

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        email = extract_field_from_body('email', body)
        password = extract_field_from_body('password', body)
        nickname = extract_field_from_body('nickname', body)

        user_id = database.insert_user(
            db_connection, email, password, nickname)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps({"id": user_id}), status=201, mimetype='application/json')


@app.route('/quizzes', methods=['POST'])
def create_quiz():

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        user_id = extract_field_from_body('user_id', body)
        short_url = extract_field_from_body('short_url', body)
        question = extract_field_from_body('question', body)
        answers_target = extract_field_from_body('answers_target', body)

        quiz_id = database.insert_quiz(
            db_connection, user_id, short_url, question, answers_target)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps({"id": quiz_id}), status=201, mimetype='application/json')


@app.route('/options', methods=['POST'])
def create_options():

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        texts = extract_field_from_body('texts', body)
        quiz_id = extract_field_from_body('quiz_id', body)

        for text in texts:
            database.insert_option(db_connection, quiz_id, text)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps({}), status=201, mimetype='application/json')


@app.route('/users', methods=['GET'])
def get_user():

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        email = extract_field_from_body('email', body)

        user = database.get_user_by_email(db_connection, email)

        data = {
            'id': user[0],
            'email': user[1],
            'password': user[2],
            'activated': user[3],
            'nickname': user[4],
            'created_date': user[5]
        }

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps(data), status=201, mimetype='application/json')


@app.route('/users/activate', methods=['POST'])
def activate_user():

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        token = extract_field_from_body('token', body)

        database.activate_user(db_connection, token)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response('User activated.', status=200, mimetype='application/json')


@app.route('/activation_tokens', methods=['POST'])
def create_activation_token():

    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        user_id = extract_field_from_body('user_id', body)
        token = extract_field_from_body('token', body)

        activation_token_id = database.insert_activation_token(
            db_connection, user_id, token)

    except:
        return Response("Bad request.", status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)

    return Response(json.dumps({"id": activation_token_id}), status=201, mimetype='application/json')


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
