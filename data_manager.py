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

