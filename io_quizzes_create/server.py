from flask import Flask, request, Response, json
from utils import extract_field_from_body
import database


app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
