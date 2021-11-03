from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def add_question(cursor, question):
    query = f"""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES('{question["submission_time"]}',
                    '{question["view_number"]}',
                    '{question["vote_number"]}',
                    '{question["title"]}',
                    '{question["message"]}',
                    '{question["image"]}')"""
    cursor.execute(query)

