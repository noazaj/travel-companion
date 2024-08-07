import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL')

def connect_pg():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as err:
        print(f'Error connecting to database: {err}')
