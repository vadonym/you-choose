from flask import Flask, request, Response, json
from utils import extract_field_from_body, generate_activation_token, get_user
import io_service
import email_service
import security

app = Flask(__name__)


@app.route('/api/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


@app.route('/api/users/activate/<token>', methods=['GET'])
def activate_user(token):
    try:

        data = {
            'token': token
        }

        code, _ = io_service.post('/users/activate', data)

        if code == 200:
            return Response('User activated.', status=201, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


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

            data = {
                'email': email,
                'token': activation_token
            }

            email_service.get('/', data)

            return Response(json.dumps(res), status=201, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


@app.route('/api/quizzes', methods=['POST'])
def create_quiz():

    try:
        user = get_user(request)

        body = request.get_json()
        question = extract_field_from_body('question', body)
        short_url = extract_field_from_body('short_url', body)
        answers_target = extract_field_from_body('answers_target', body)
        texts = extract_field_from_body('texts', body)

        data = {
            'user_id': user['id'],
            'question': question,
            'short_url': short_url,
            'answers_target': answers_target
        }

        texts = list(filter(lambda text: text != "", texts))

        if len(texts) < 2:
            raise Exception("Invalid number of options")

        _, res = io_service.post('/quizzes', data)

        quiz_id = res['id']

        data = {
            'quiz_id': quiz_id,
            'texts': texts
        }

        io_service.post('/options', data)

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')

    return Response(json.dumps({'id': quiz_id}), status=201, mimetype='application/json')


@app.route('/api/quizzes/short_url/<short_url>', methods=['GET'])
def get_quiz_by_short_url(short_url):
    try:
        user = get_user(request)

        data = {
            'user_id': user['id']
        }

        code, res = io_service.get(f'/quizzes/short_url/{short_url}', data)

        if code == 200:
            return Response(json.dumps(res), status=200, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


@app.route('/api/quizzes/<id>', methods=['GET'])
def get_quiz(id):
    try:
        user = get_user(request)

        data = {
            'user_id': user['id']
        }

        code, res = io_service.get(f'/quizzes/{id}', data)

        if code == 200:
            return Response(json.dumps(res), status=200, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


@app.route('/api/quizzes/<quiz_id>/answer', methods=['POST'])
def answer_quiz(quiz_id):
    try:
        user = get_user(request)

        body = request.get_json()
        option_id = extract_field_from_body('option_id', body)

        data = {
            'user_id': user['id'],
            'option_id': option_id
        }

        code, _ = io_service.post(f'/quizzes/{quiz_id}/answer', data)

        if code == 201:
            return Response('Answer added.', status=201, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
