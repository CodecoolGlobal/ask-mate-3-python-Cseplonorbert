from typing import List, Dict
import utils

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_bonus_questions(cursor):
    query = f"""SELECT * FROM bonus_question"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, question):
    query = f"""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
            VALUES(CURRENT_DATE,
                    '{question.get("view_number", 0)}',
                    '{question.get("vote_number", 0)}',
                    '{question["title"]}',
                    '{question["message"]}',
                    '{question.get("image", "")}',
                    '{question["user_id"]}')"""
    cursor.execute(query)


@database_common.connection_handler
def add_new_answer(cursor, answer):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
        VALUES(CURRENT_DATE,
                '{answer.get("vote_number", 0)}',
                '{answer.get("question_id", 0)}',
                '{answer["message"]}',
                '{answer.get("image", "")}',
                '{answer.get("user_id")}')"""
    cursor.execute(query)


@database_common.connection_handler
def delete_question_id(cursor, question_id):
    query = f"""
        DELETE FROM question 
        WHERE question.id = '{question_id}'
        """

    cursor.execute(query)


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = f"""
        DELETE FROM answer 
        WHERE answer.id = '{answer_id}'
        """

    cursor.execute(query)


@database_common.connection_handler
def add_answer_comment(cursor, answer_comment):
    query = f"""
    INSERT 
    INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id) 
    VALUES(NULL, '{answer_comment["answer_id"]}', '{answer_comment["message"]}',
    CURRENT_DATE, '{answer_comment["edited_count"]}', '{answer_comment["user_id"]}')"""
    cursor.execute(query)


@database_common.connection_handler
def get_questions(cursor):
    query = f"""SELECT question.id,
       question.submission_time,
       view_number,
       vote_number,
       title,
       message,
       image,
       user_id,
       users.email
        FROM question
        JOIN users ON question.user_id = users.id;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = f"""SELECT question.id,
                question.submission_time,
                view_number,
                vote_number,
                title,
                message,
                image,
                user_id,
                users.email
                FROM question
                JOIN users ON question.user_id = users.id
                WHERE question.id = '{question_id}'"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def answers_by_question_id(cursor, question_id):
    query = f"""SELECT answer.id,
       answer.submission_time,
       question_id,
       vote_number,
       message,
       image,
       user_id,
       users.email,
       accepted
        FROM answer
        JOIN users ON answer.user_id = users.id
        WHERE question_id ='{question_id}' ORDER BY answer.submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def edit_answer(cursor, answer, answer_id):
    query = f"""
            UPDATE answer SET
            submission_time = CURRENT_DATE,
            vote_number = 0,
            message = '{answer.get("message")}',
            image = '{answer.get("image", "")}'
            WHERE answer.id ='{answer_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = f"""SELECT * FROM answer WHERE id='{answer_id}'"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def edit_question(cursor, question, question_id):
    query = f"""
            UPDATE question SET 
            submission_time = CURRENT_DATE,
            title = '{question["title"]}',
            message = '{question["message"]}',
            image = '{question.get("image", "")}'
            WHERE question.id ='{question_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def increase_vote_number(cursor, table, row_id):
    query = f"""
            UPDATE {table} 
            SET vote_number = vote_number + 1
            WHERE id = '{row_id}' 
    """
    cursor.execute(query)


@database_common.connection_handler
def decrease_vote_number(cursor, table, row_id):
    query = f"""
            UPDATE {table} 
            SET vote_number = vote_number - 1
            WHERE id = '{row_id}'
    """
    cursor.execute(query)


@database_common.connection_handler
def increase_view(cursor, question_id):
    query = f"""
            UPDATE question 
            SET view_number = view_number + 1 
            WHERE id = '{question_id}'
    """
    cursor.execute(query)


@database_common.connection_handler
def search_question(cursor, search_phrase):
    query = f"""
            SELECT id, submission_time, view_number, vote_number, title, message
            FROM question
            WHERE title ILIKE '%{search_phrase}%' or message ILIKE '%{search_phrase}%' 
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def edit_comment(cursor, edited_comment):
    query = f"""
         UPDATE comment
         SET message = '{edited_comment["message"]}', submission_time = CURRENT_DATE,
         edited_count = edited_count + 1 
         WHERE id = '{edited_comment["id"]}'
         """
    cursor.execute(query)


@database_common.connection_handler
def display_latest_questions(cursor, number_of_questions=5):
    query = f"""SELECT question.id,
        question.submission_time,
        view_number,
        vote_number,
        title,
        message,
        image,
        user_id,
        users.email
        FROM question
        JOIN users ON question.user_id = users.id
        ORDER BY submission_time 
        LIMIT '{number_of_questions}'"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def sort_questions(cursor, order_by, order):
    query = f"""SELECT * FROM question ORDER BY {order_by} {order}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_tag(cursor, tag_name):
    pass


@database_common.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    pass


@database_common.connection_handler
def get_question_tags(cursor, question_id):
    pass


@database_common.connection_handler
def get_tags(cursor):
    pass


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    pass


@database_common.connection_handler
def get_comments(cursor):
    query = """SELECT comment.id,
       comment.submission_time,
       comment.question_id,
       comment.answer_id,
       message,
       edited_count,
       user_id,
       users.email
        FROM comment
        JOIN users ON comment.user_id = users.id
        ORDER BY comment.submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question_comment(cursor, comment):
    query = f"""
        INSERT 
        INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id) 
        VALUES('{comment["question_id"]}', NULL, '{comment["message"]}',
        CURRENT_DATE, '{comment["edited_count"]}', '{comment["user_id"]}')"""
    cursor.execute(query)


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    query = f"""
       DELETE
       FROM comment
       WHERE id = '{comment_id}'
       """
    cursor.execute(query)


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = f"""SELECT * FROM comment WHERE id='{comment_id}'"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_user_data(cursor, user_id):
    cursor.execute("""
                SELECT * FROM users
                WHERE id = %(u_i)s""",
                   {'u_i': int(user_id)})
    user_data = cursor.fetchone()
    return user_data


@database_common.connection_handler
def get_related_answers(cursor, user_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE user_id = %(u_i)s""",
                   {'u_i': int(user_id)})
    related_answers = cursor.fetchall()
    return related_answers


@database_common.connection_handler
def get_related_questions(cursor, user_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE user_id = %(u_i)s""",
                   {'u_i': int(user_id)})
    related_questions = cursor.fetchall()
    return related_questions


@database_common.connection_handler
def get_related_comments(cursor, user_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE user_id = %(u_i)s""",
                   {'u_i': int(user_id)})
    related_comments = cursor.fetchall()
    return related_comments


@database_common.connection_handler
def count_related_questions(cursor, user_id):
    cursor.execute("""
                    SELECT COUNT(user_id) FROM question
                    WHERE user_id = %(u_i)s""",
                   {'u_i': int(user_id)})
    number_of_related_questions = cursor.fetchone()
    return number_of_related_questions


@database_common.connection_handler
def count_related_answers(cursor, user_id):
    cursor.execute("""
                    SELECT COUNT(user_id) FROM answer
                    WHERE user_id = %(u_i)s""",
                   {'u_i': int(user_id)})
    number_of_related_answers = cursor.fetchone()
    return number_of_related_answers


@database_common.connection_handler
def count_related_comments(cursor, user_id):
    cursor.execute("""
                    SELECT COUNT(user_id) FROM comment
                    WHERE user_id = %(u_i)s""",
                   {'u_i': int(user_id)})
    number_of_related_comments = cursor.fetchone()
    return number_of_related_comments


@database_common.connection_handler
def get_user_info(cursor, email):
    cursor.execute("""
        SELECT * FROM users
        WHERE email = %(e_l)s""", {'e_l': email})

    return cursor.fetchall()


@database_common.connection_handler
def registrate_user(cursor, email, password):
    query = f"""
        INSERT
        INTO users (email, password, submission_time, reputation)
        VALUES ('{email}', '{password}', NOW(), 0)
        """
    cursor.execute(query)


@database_common.connection_handler
def increase_reputation(cursor, table, user_id):
    if table == "question":
        query = f"""
                UPDATE users 
                SET reputation = reputation + 5
                WHERE users.id = {user_id}
        """
    elif table == "answer":
        query = f"""
                UPDATE users
                SET reputation = reputation + 10
                WHERE users.id = {user_id}
        """
    cursor.execute(query)


@database_common.connection_handler
def decrease_reputation(cursor, user_id):
    query = f"""
            UPDATE users 
            SET reputation = reputation - 2
            WHERE users.id = {user_id}
    """
    cursor.execute(query)
  
 
@database_common.connection_handler    
def get_all_user_data(cursor):
    query = """
    SELECT
    users.id as user_id, 
    users.email AS username,
    users.submission_time AS registration_date,
    COUNT(DISTINCT question.message) AS number_of_asked_questions,
    COUNT(DISTINCT comment.message) AS number_of_comments,
    COUNT(DISTINCT answer.message) AS number_of_answers,
    users.reputation
    FROM users 
    LEFT JOIN question ON users.id = question.user_id
    LEFT JOIN comment ON comment.user_id = users.id
    LEFT JOIN answer ON users.id = answer.user_id
    GROUP BY users.email,users.submission_time,users.reputation,users.id
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def accept_answer(cursor, answer_id):
    query = f"""
       UPDATE answer
       SET accepted = true
       WHERE id = '{answer_id}'
       """
    cursor.execute(query)


@database_common.connection_handler
def remove_accept(cursor, answer_id):
    query = f"""
       UPDATE answer
       SET accepted = false
       WHERE id = '{answer_id}'
           """
    cursor.execute(query)


@database_common.connection_handler
def increase_reputation_for_acceptance(cursor, user_id):
    query = f"""
        UPDATE users 
        SET reputation = reputation+15
        WHERE id = '{user_id}' 
              """
    cursor.execute(query)
