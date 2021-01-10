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


def get_quiz(connection, id, user_id):
    cursor = connection.cursor()

    sql = "SELECT id, user_id, short_url, question, answers_target FROM quizzes WHERE id = %s"
    val = (id,)

    sql_options = "SELECT id, text FROM t_options WHERE quiz_id = %s"
    val_options = (id,)

    sql_answered = "SELECT COUNT(*) FROM answers WHERE quiz_id = %s AND user_id = %s"
    val_answered = (id, user_id)

    sql_result = "SELECT option_id FROM results WHERE quiz_id = %s"
    val_result = (id,)

    data = dict()

    try:
        cursor.execute(sql, val)

        quiz = cursor.fetchone()
        data['id'] = quiz[0]
        data['short_url'] = quiz[2]
        data['question'] = quiz[3]

        cursor.execute(sql_options, val_options)
        db_options = cursor.fetchall()
        options = []

        for db_option in db_options:
            options.append({
                'id': db_option[0],
                'text': db_option[1]
            })

        data['options'] = options

        cursor.execute(sql_answered, val_answered)
        data['answered'] = (cursor.fetchone()[0] == 1)

        cursor.execute(sql_result, val_result)
        result = cursor.fetchone()

        if result == None:
            data['has_result'] = False
        else:
            data['has_result'] = True
            data['result'] = result[0]

        return data
    except:
        connection.rollback()
        raise Exception()

    cursor.close()


def get_quiz_id(connection, short_url):
    cursor = connection.cursor()

    sql = "SELECT id FROM quizzes WHERE short_url = %s"
    val = (short_url,)

    try:
        cursor.execute(sql, val)
        connection.commit()

        return cursor.fetchone()[0]

    except:
        connection.rollback()
        raise Exception()

    cursor.close()


def answer(connection, quiz_id, user_id, option_id):
    cursor = connection.cursor()

    sql = "INSERT INTO answers (user_id, quiz_id, option_id) VALUES (%s, %s, %s)"
    val = (quiz_id, user_id, option_id)

    try:
        cursor.execute(sql, val)
        connection.commit()

    except:
        connection.rollback()
        raise Exception()

    cursor.close()


def result(connection, quiz_id):
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM answers WHERE quiz_id = %s"
    val = (quiz_id,)

    sql_req = "SELECT answers_target FROM quizzes WHERE id = %s"
    val_req = (quiz_id,)

    sql_res = "SELECT count(*) as cnt, option_id FROM answers WHERE quiz_id = %s GROUP BY option_id ORDER BY cnt DESC"
    val_res = (quiz_id,)

    sql_add_res = "INSERT INTO results (quiz_id, option_id) VALUES (%s, %s)"

    try:
        cursor.execute(sql, val)
        answer_count = cursor.fetchone()[0]

        cursor.execute(sql_req, val_req)
        answers_target = cursor.fetchone()[0]

        if answer_count == answers_target:
            cursor.execute(sql_res, val_res)
            result_id = cursor.fetchall()[0][1]

            val_add_res = (quiz_id, result_id)
            cursor.execute(sql_add_res, val_add_res)
            connection.commit()

    except:
        connection.rollback()
        raise Exception()

    cursor.close()
