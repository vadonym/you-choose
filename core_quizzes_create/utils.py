import auth_service

ACTIVATION_TOKEN_LENGTH = 64


def extract_field_from_body(field, body):
    return body[field] if field in body else None


def get_user(request):
    token = request.headers.get('Authorization').split(" ")[1]

    data = {
        'token': token
    }

    code, res = auth_service.get("/auth", data)

    if code != 200:
        raise Exception(res)

    return res
