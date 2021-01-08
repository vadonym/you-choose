import secrets

ACTIVATION_TOKEN_LENGTH = 64


def extract_field_from_body(field, body):
    return body[field] if field in body else None


def generate_activation_token():
    return secrets.token_urlsafe(ACTIVATION_TOKEN_LENGTH)[:ACTIVATION_TOKEN_LENGTH]
