from flask import Flask, jsonify, render_template, json
import psycopg2
from flask_sqlalchemy import SQLAlchemy 
from decouple import config



def create_app():
    
    app=Flask(__name__)

     # connect to the PostgreSQL server
    conn = psycopg2.connect("postgres://" + config("POSTGRES_USERNAME") + ":" + config("POSTGRES_PASSWORD") + "@raja.db.elephantsql.com:5432/mozfsrjp")

    @app.route('/')
    def hello():
        """Homepage, returns a string"""
        return "Hello world"


    @app.route('/topcomments')
    def topcomments():
        """Returns 100 most salty comments"""
        cur=conn.cursor()
        cur.execute("(SELECT ROW_TO_JSON(c) FROM (SELECT * FROM comments ORDER BY saltiness DESC LIMIT 100) c)")
        result_set=cur.fetchall()
        final=[]
        for i in range(len(result_set)):
            final.append(result_set[i][0])
        
        return json.dumps(final) 

    query='''SELECT ROW_TO_JSON(t) FROM (SELECT author, 
    COUNT(*) as n_comments, 
    AVG(saltiness) as avg_salt 
    FROM comments 
    GROUP BY author) AS t
    WHERE t.n_comments>50 
    ORDER BY t.avg_salt DESC
    LIMIT 100
    '''

    @app.route('/topusers')
    def topusers():
        """Returns top 100 saltiest users (using AVG(saltiness)) of their comments
        Limited to users with 50+ comments overall"""
        cur=conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        final=[]
        for i in range(len(result)):
            final.append(result[i][0])
        return json.dumps(final)

    return app
