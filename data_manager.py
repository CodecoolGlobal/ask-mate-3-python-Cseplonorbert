from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_ommon.connection_handler
def add_question(cursor, submission_time, view_number, vote_number, title, message, image):
    query = f"""
            INSERT INTO question
            VALUES('{submission_time}', '{view_number}', '{vote_number}', '{title}','{message}', '{image}')
            """
    cursor.execute(query)
    return cursor.fetchall()

