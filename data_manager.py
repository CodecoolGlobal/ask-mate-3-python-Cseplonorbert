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
def add_answer_comment(cursor, answer_comment, question_id, answer_id):
    query = f"""
    INSERT 
    INTO comment (question_id, answer_id, message, submission_time, edited_count) 
    VALUES('{question_id}', '{answer_id}', '{answer_comment["message"]}',
    CURRENT_DATE, '{answer_comment["edited_count"]}'"""
    cursor.execute(query)


@database_common.connection_handler
def edit_question(cursor, question):
    pass


@database_common.connection_handler
def vote_data(cursor, datatype, data_id, vote):
    pass


@database_common.connection_handler
def increase_view(cursor, question_id):
    pass
