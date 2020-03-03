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


    # app.route('/topx')
    # def topx():
    #     cur=conn.cursor()
    #     cur.execute("SELECT DISTINCT ")
    #     cur.fetchall()
    #     return "Hello"

    return app
