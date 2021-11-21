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
    val = (user_id, quiz_id, option_id)

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
