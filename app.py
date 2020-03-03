from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, render_template, redirect, request

from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_URL = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

app = Flask(__name__)

# STILL TRYING TO FIGURE OUT HOW SQLALCHEMY WORKS
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# db = SQLAlchemy()

@app.route('/<username>')
def username(username=None):
    '''
    returns json output of saltiness score for given username
    '''

    query = f'''
    SELECT *
    FROM comments
    WHERE author = '{username}'
    ORDER BY saltiness DESC
    LIMIT 100
    '''

    conn = psycopg2.connect(DB_URL)
    curs = conn.cursor()
    curs.execute(query)
    headers = ['c_id', 'u_id', 'timestamp', 'comment_text', 'p_id', 'saltiness']
    results = curs.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)
