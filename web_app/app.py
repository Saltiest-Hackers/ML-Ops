from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from psycopg2 import connect

load_dotenv()

app = Flask(__name__)

# STILL TRYING TO FIGURE OUT HOW SQLALCHEMY WORKS
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# db = SQLAlchemy()

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_URL = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
conn = connect(DB_URL)

@app.route('/user/<username>')
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

    curs = conn.cursor()
    curs.execute(query)
    headers = ['c_id', 'u_id', 'timestamp', 'comment_text', 'p_id', 'saltiness']
    results = curs.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))

    return jsonify(json_data)
