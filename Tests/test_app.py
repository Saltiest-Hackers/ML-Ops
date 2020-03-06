from psycopg2 import connect
from requests import get


DB_USER = config('POSTGRES_USERNAME')
DB_PASS = config('POSTGRES_PASSWORD')
DB_HOST = config('POSTGRES_HOST')
DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_USER}'

def test_username():
    return

def test_comment():
    return