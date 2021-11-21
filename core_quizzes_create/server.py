from flask import Flask, request, Response, json
from utils import extract_field_from_body, get_user
import io_quizzes_create_service

app = Flask(__name__)


@app.route('/api/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


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

        _, res = io_quizzes_create_service.post('/quizzes', data)

        quiz_id = res['id']

        data = {
            'quiz_id': quiz_id,
            'texts': texts
        }

        io_quizzes_create_service.post('/options', data)

    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')

    return Response(json.dumps({'id': quiz_id}), status=201, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
