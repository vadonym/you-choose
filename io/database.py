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


def activate_user(connection, user_id):
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
