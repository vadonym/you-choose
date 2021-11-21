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


def insert_quiz(connection, user_id, short_url, question, answers_target):
    cursor = connection.cursor()

    sql = "INSERT INTO quizzes (user_id, short_url, question, answers_target) VALUES (%s, %s, %s, %s) RETURNING id"
    val = (user_id, short_url, question, answers_target)

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
