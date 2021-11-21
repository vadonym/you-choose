from flask import Flask, request, Response, json
from utils import extract_field_from_body, generate_activation_token, get_user
import io_quizzes_query_service

app = Flask(__name__)


@app.route('/api/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


@app.route('/api/quizzes/short_url/<short_url>', methods=['GET'])
def get_quiz_by_short_url(short_url):
    try:
        user = get_user(request)

        data = {
            'user_id': user['id']
        }

        code, res = io_quizzes_query_service.get(
            f'/quizzes/short_url/{short_url}', data)

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

        code, res = io_quizzes_query_service.get(f'/quizzes/{id}', data)

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

        code, _ = io_quizzes_query_service.post(
            f'/quizzes/{quiz_id}/answer', data)

        if code == 201:
            return Response('Answer added.', status=201, mimetype='application/json')

        return Response('Bad request.', status=400, mimetype='application/json')

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
