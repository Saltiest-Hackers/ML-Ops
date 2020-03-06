from psycopg2 import connect
from decouple import config
from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    
    app=Flask(__name__)
    CORS(app)

    DB_USER = config('POSTGRES_USERNAME')
    DB_PASS = config('POSTGRES_PASSWORD')
    DB_HOST = config('POSTGRES_HOST')
    DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_USER}'

    @app.route('/')
    def hello():

        return 'Hello world'


    @app.route('/topcomments')
    def topcomments():
        '''
        Returns 100 most salty comments
        '''

        query = '''
        SELECT *
        FROM comments
        ORDER BY saltiness DESC
        LIMIT 100
        '''
        with connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                headers = [x[0] for x in cur.description]
        
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        
        return jsonify(json_data)



    @app.route('/topusers')
    def topusers():
        '''
        Returns top 100 saltiest users (using AVG(saltiness)) of their comments
        Limited to users with 50+ comments overall
        '''
        
        query = '''
        SELECT *
        FROM (
            SELECT
                author, 
                COUNT(author) AS n_comments,
                AVG(saltiness) AS avg_salt
            FROM comments
            GROUP BY author
            ) t
        WHERE t.n_comments > 50
        ORDER BY t.avg_salt DESC
        LIMIT 100
        '''
        with connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                headers = [x[0] for x in cur.description]
        
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        
        return jsonify(json_data)


    @app.route('/user/<username>')
    def username(username=None):
        '''
        returns json output of saltiness score for given username
        '''
        try:
            query = f'''
            SELECT *
            FROM comments
            WHERE author = '{username}'
            ORDER BY saltiness DESC
            LIMIT 100
            '''
            with connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    headers = [x[0] for x in cur.description]
                    results = cur.fetchall()
        
            json_data = []
            for result in results:
                json_data.append(dict(zip(headers, result)))

            return jsonify(json_data)
        
        except:
            return jsonify({'message': 'User Not Found'})



    @app.route('/comment/<comment_id>')
    def comment(comment_id=None):
        '''
        returns json of comment text, given comment id
        '''

        try:
            query = f'''
            SELECT *
            FROM comments
            WHERE id = '{comment_id}'
            '''
            with connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    headers = [x[0] for x in cur.description]
                    result = cur.fetchone()
        
            return jsonify(dict(zip(headers, result)))

        except:
            return jsonify({'message': 'Comment ID Not Found'})

    return app
