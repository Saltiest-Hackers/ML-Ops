from psycopg2 import connect
from decouple import config
from flask import Flask, jsonify, render_template, json
import psycopg2
from flask_sqlalchemy import SQLAlchemy 
from decouple import config



def create_app():
    
    app=Flask(__name__)

    DB_USER = config('POSTGRES_USERNAME')
    DB_PASS = config('POSTGRES_PASSWORD')
    DB_HOST = config('POSTGRES_HOST')
    DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_USER}'
    conn = connect(DB_URL)

    @app.route('/')
    def hello():
        '''Homepage, returns a string'''

        return 'Hello world'


    @app.route('/topcomments')
    def topcomments():
        '''Returns 100 most salty comments'''

        query = '''
        SELECT ROW_TO_JSON(c) 
        FROM (SELECT * FROM comments ORDER BY saltiness DESC LIMIT 100) c
        '''
        cur = conn.cursor()
        cur.execute(query)
        result_set=cur.fetchall()
        final=[]
        for i in range(len(result_set)):
            final.append(result_set[i][0])
        
        return jsonify(final)



    @app.route('/topusers')
    def topusers():
        '''Returns top 100 saltiest users (using AVG(saltiness)) of their comments
        Limited to users with 50+ comments overall'''
        
        query = '''
        SELECT ROW_TO_JSON(t) FROM (SELECT author, 
        COUNT(*) as n_comments, 
        AVG(saltiness) as avg_salt 
        FROM comments 
        GROUP BY author) AS t
        WHERE t.n_comments>50 
        ORDER BY t.avg_salt DESC
        LIMIT 100
        '''
        cur=conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        final=[]
        for i in range(len(result)):
            final.append(result[i][0])
        
        return jsonify(final)


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
        headers = [x[0] for x in curs.description]
        results = curs.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))

        return jsonify(json_data)

    return app
