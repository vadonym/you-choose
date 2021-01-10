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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
