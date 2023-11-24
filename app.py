from flask import Flask, render_template, request, flash, redirect, session, g, sessions
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests, json
import json
import pandas as pd
# from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql:///jeffreyng'
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"
# toolbar = DebugToolbarExtension(app)

api_key = '1288b79b'


connect_db(app)

@app.route('/')
def home():
    df = pd.read_json('~/IMDB_IDs/IMDB.json')
    url= 'http://www.omdbapi.com/?&i='
    movies = df.movies
    print(len(movies))
    list_of_movies=[]
    for x in movies[0:1]:
        try:
            resp = requests.get('http://www.omdbapi.com/?apikey=1288b79b&?i={}'.format(x))
            print(resp.text)
            list_of_movies.append(resp.text)
        except:
            pass
    return render_template('home.html', list_of_movies = list_of_movies)



