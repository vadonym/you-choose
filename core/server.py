from flask import Flask, request, Response, json
from utils import extract_field_from_body, generate_activation_token
import io_service
import security

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


@app.route('/api/users', methods=['POST'])
def create_user():

    try:
        body = request.get_json()

        email = extract_field_from_body('email', body)
        password = extract_field_from_body('password', body)
        nickname = extract_field_from_body('nickname', body)

        if email == None:
            raise Exception('Field email is missing.')
        if password == None:
            raise Exception('Field password is missing.')
        if nickname == None:
            raise Exception('Field nickname is missing.')

        data = {
            'email': email,
            'password': security.hash_password(password),
            'nickname': nickname
        }

        code, res = io_service.post('/users', data)

        if code == 201:
            activation_token = generate_activation_token()

            data = {
                'user_id': res['id'],
                'token': activation_token
            }

            io_service.post('/activation_tokens', data)

            return Response(json.dumps(res), status=201, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
