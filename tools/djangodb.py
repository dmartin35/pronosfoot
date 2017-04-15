"""
DJANGO DB TOOLS MODULE
"""
from django.db import connection


def executeRawSqlQuery(query):
    """
    executes a SQL query and returns the result
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
