# utils.py
from django.db import connection

def fetch_table_data(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM "{table_name}"')
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return columns, rows
