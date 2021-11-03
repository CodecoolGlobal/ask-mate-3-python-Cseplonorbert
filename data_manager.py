from typing import List, Dict
import utils

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def add_question(cursor, question):
    query = f"""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES(CURRENT_DATE,
                    '{question.get("view_number", 0)}',
                    '{question.get("vote_number", 0)}',
                    '{question["title"]}',
                    '{question["message"]}',
                    '{question.get("image", "")}')"""
    cursor.execute(query)


@database_common.connection_handler
def add_new_answer(cursor, answer):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES(CURRENT_DATE,
                '{answer.get("vote_number",0)}',
                '{answer.get("question_id", 0)}',
                '{answer["message"]}',
                '{answer.get("image", "")}')"""
    cursor.execute(query)


@database_common.connection_handler
def add_answer_comment(cursor, answer_comment, answer_id):
    query = f"""
    INSERT 
    INTO comment (question_id, answer_id, message, submission_time, edited_count) 
    VALUES(NULL, '{answer_id}', '{answer_comment["message"]}',
    CURRENT_DATE, '{answer_comment["edited_count"]}'"""
    cursor.execute(query)


@database_common.connection_handler
def get_questions(cursor):
    pass


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    pass


@database_common.connection_handler
def answers_by_question_id(cursor, question_id):
    pass


@database_common.connection_handler
def edit_question(cursor, question):
    pass


@database_common.connection_handler
def vote_data(cursor, datatype, data_id, vote):
    pass


@database_common.connection_handler
def increase_view(cursor, question_id):
    pass


@database_common.connection_handler
def search_question(cursor, search_phrase):
    pass


@database_common.connection_handler
def edit_comment(cursor, edited_comment):
    pass


@database_common.connection_handler
def display_latest_questions(cursor, number_of_questions=5):
    pass


@database_common.connection_handler
def sort_questions(cursor, order_by, order):
    pass


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    pass


@database_common.connection_handler
def get_comments(cursor):
    query = """SELECT question_id, answer_id, message, submission_time, edited_count FROM comment"""
    cursor.execute(query)
    cursor.fetchall()


@database_common.connection_handler
def add_new_question_comment(cursor, comment, question_id):
    query = f"""
        INSERT 
        INTO comment (question_id, answer_id, message, submission_time, edited_count) 
        VALUES('{question_id}', NULL, '{comment["message"]}',
        CURRENT_DATE, '{comment["edited_count"]}'"""
    cursor.execute(query)
