import psycopg2
from get_docker_secret import get_docker_secret
import os


def create_database_connection():
    connection = psycopg2.connect(user=get_docker_secret(os.environ['DATABASE_USER']),
                                  password=get_docker_secret(
                                      os.environ['DATABASE_PASSWORD']),
                                  host="database",
                                  port="5432",
                                  database=get_docker_secret(os.environ['DATABASE_DB']))
    return connection


def close_connection(connection):
    connection.close()


def insert_user(connection, email, password, nickname):
    cursor = connection.cursor()

    sql = "INSERT INTO users (email, password, nickname) VALUES (%s, %s, %s) RETURNING id"
    val = (email, password, nickname)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception()

    user_id = cursor.fetchone()[0]

    cursor.close()

    return user_id


def insert_quiz(connection, user_id, short_url, question, heuristic_id, answers_target):
    cursor = connection.cursor()

    sql = "INSERT INTO quizzes (user_id, short_url, question, heuristic_id, answers_target) VALUES (%s, %s, %s, %s, %s) RETURNING id"
    val = (user_id, short_url, question, heuristic_id, answers_target)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception()

    user_id = cursor.fetchone()[0]

    cursor.close()

    return user_id


def insert_option(connection, quiz_id, text):
    cursor = connection.cursor()

    sql = "INSERT INTO t_options (quiz_id, text) VALUES (%s, %s)"
    val = (quiz_id, text)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception()

    cursor.close()


def insert_activation_token(connection, user_id, token):
    cursor = connection.cursor()

    sql = "INSERT INTO activation_tokens (user_id, token) VALUES (%s, %s) RETURNING id"
    val = (user_id, token)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception()

    activation_token_id = cursor.fetchone()[0]

    cursor.close()

    return activation_token_id


def get_user_id_by_token(connection, token):
    cursor = connection.cursor()

    sql = "SELECT user_id FROM activation_tokens WHERE token = %s"
    val = (token,)

    try:
        cursor.execute(sql, val)
        connection.commit()

        return cursor.fetchone()[0]

    except:
        connection.rollback()
        raise Exception()

    cursor.close()


def activate_user(connection, token):
    user_id = get_user_id_by_token(connection, token)

    cursor = connection.cursor()

    sql_users = "UPDATE users SET activated = True WHERE id = %s"
    val_users = (user_id,)

    sql_activation_tokens = "DELETE FROM activation_tokens WHERE user_id = %s"
    val_activation_tokens = (user_id,)

    try:
        cursor.execute(sql_users, val_users)
        cursor.execute(sql_activation_tokens, val_activation_tokens)

        connection.commit()

    except:
        connection.rollback()
        raise Exception()

    cursor.close()


def get_user_by_email(connection, email):
    cursor = connection.cursor()

    sql = "SELECT * FROM users WHERE email = %s"
    val = (email,)

    try:
        cursor.execute(sql, val)
        connection.commit()

        return cursor.fetchone()

    except:
        connection.rollback()
        raise Exception()

    cursor.close()
