from flask import Flask, jsonify, render_template, json
import psycopg2
from flask_sqlalchemy import SQLAlchemy 
from decouple import config

def create_app():
    
    app=Flask(__name__)


    @app.route('/')
    def hello():
        # connect to the PostgreSQL server
        conn = psycopg2.connect("postgres://" + config("POSTGRES_USERNAME") + ":" + config("POSTGRES_PASSWORD") + "@raja.db.elephantsql.com:5432/mozfsrjp")
        message="Hello, world"
        cur=conn.cursor()
        cur.execute("(SELECT ROW_TO_JSON(c) FROM (SELECT * FROM comments ORDER BY saltiness DESC LIMIT 100) c)")
        # cur.execute("SELECT * FROM comments ORDER BY saltiness DESC LIMIT 100")
        result_set=cur.fetchall()
        final=[]

        for i in range(len(result_set)):
            #print(result_set[i][0])
            final.append(result_set[i][0])
        
        return json.dumps(final) 


    # app.route('/topx')
    # def topx():
    #     conn = psycopg2.connect("postgres://" + config("POSTGRES_USERNAME") + ":" + config("POSTGRES_PASSWORD") + "@raja.db.elephantsql.com:5432/mozfsrjp")
    #     message="Hello"
    #     cur=conn.cursor()
    #     x=100
    #     cur.execute("(SELECT ROW_TO_JSON(c) FROM (SELECT * FROM comments LIMIT 10) c)")
    #     cur.fetchall()
    #     return message


   


    return app



#Trying to use SQLAlchemy: 

    # DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=config("POSTGRES_USERNAME"),pw=config("POSTGRES_PASSWORD"),url=config("POSTGRES_URL"),db=config("POSTGRES_DB"))

    # app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

    # DB = SQLAlchemy(app)    

    # DB.init_app(app)

    # class Comment(DB.Model):
    #     id = DB.Column(DB.Integer, primary_key=True)
    #     author = DB.Column(DB.String)
    #     comment_text = DB.Column(DB.Unicode)


    # @app.route('/')
    # def hello():
    #     comments = Comment.query.limit(5).all()
    #     return render_template("home.html", comments=comments)