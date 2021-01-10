from flask import Flask, request, Response
from email_utils import send_activation_link

app = Flask(__name__)


@app.route('/')
def send():
    try:
        body = request.get_json()

        email = body['email']
        token = body['token']

        send_activation_link(email, token)

        return Response("Activation link sent.", status=201, mimetype='application/json')
    except:
        return Response("Sending activation link failed.", status=400, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
