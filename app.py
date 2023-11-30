from flask import Flask, render_template, request, flash, redirect, session
# from flask_session import Session
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
import requests, json
import ast
import json
import pickle
from collections.abc import Mapping
import pandas as pd
from forms import MovieForm, CatalogForm, UserAddForm, LoginForm
from models import db, connect_db, Movie, Tag, User, Favorite, Watched


        
app = Flask(__name__)
app.app_context().push()
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql:///jeffreyng'
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"
# toolbar = DebugToolbarExtension(app)




connect_db(app)

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():

    form = UserAddForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.password.data
        
        user=User.register(username, password, email)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return redirect("/intro")

    else:
        return render_template('signup.html', form=form)
   
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        username= form.username.data
        pwd=form.password.data

        u = User.authenticate(username,
                                 pwd)

        if u:
            session["user_id"] =u.id.__dict__
            valobj=ast.literal_eval(repr(session['user_id']))
            session["username"]=u.username.__dict__
            flash(f"Hello, {u.username}!", "success")
            return redirect("/intro")

        else:
            return (f'IT DIDNT WORK!!')
            
    return render_template('login.html', form=form)

@app.route('/intro', methods=['GET', 'POST'])
def intro():

    # hello=ast.literal_eval(repr(session['user_id']))
    return render_template('intro.html')


@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    form = MovieForm()
    if form.validate_on_submit():
        term = form.title.data
        list_of_movies = Movie.query.filter(Movie.title.ilike("%" + term + "%")).all()
        if len(list_of_movies)==0:
            flash('Query found 0 results')
            return redirect('/search')
        return render_template("select.html", list_of_movies= list_of_movies)
    else:
        return render_template("search.html", form = form) 
    

@app.route('/catalog', methods=['GET', 'POST'])
def browse():

    form = CatalogForm()
    if form.validate_on_submit():
        genres = form.genres.data
        #popularitys= float(form.popularitys.data)
        # vote_averages=form.vote_average.data 
    
        #list_of_movies_by_pop = Movie.query.filter(Movie.popularity <= popularitys)
        list_of_movies_by_genres = Movie.query.filter_by(genre1 = genres)
        list_of_movies_by_genres1 = Movie.query.filter(Movie.genre2 == genres)
        # list_of_movies_by_vote_averages = Movie.query.filter(Movie.vote_average > vote_averages)
        return render_template('last_page.html', list_of_movies_by_genres=list_of_movies_by_genres,
            list_of_movies_by_genres1= list_of_movies_by_genres1)
            #list_of_movies_by_pop= list_of_movies_by_pop) 
                               #list_of_movies_by_vote_averages= list_of_movies_by_vote_averages)
    else:
        return render_template('catalog.html', form=form)

# Movie.query.filter(Movie.title.ilike("%" + term + "%")).all()
#    left inner join
# Favorites.movie.filter_by(Favorites.user_id = User.id)



@app.route("/<int:id>")
def single_movie(id):
    movie_details= Movie.query.filter(Movie.id== id)
    return render_template('movie_details.html', movie_details=movie_details)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    flash(f'LOGOUT SUCCESSFUL!!')
    return render_template('home.html')

import spacy
import numpy as np
nlp= spacy.load("en_core_web_lg")
spacy_tokenizer=nlp.tokenizer
import pandas as pd

def prep(x):
    # tokenizing=spacy_tokenizer(x) 
    embedding=nlp(x).vector.reshape(300,)
    return embedding
    
# def prepare(x):
#     # tokenizing=spacy_tokenizer(x)
#     embedding_many=nlp(x).vector.reshape(300,)
#     return embedding_many

@app.route('/recommendation/<int:id>')
def recommend_movie(id):
    movie_details= Movie.query.filter(Movie.id==id).first()
    all_movie_details= Movie.query.all()
    

    movie_details=movie_details.overview
    all_movie_detail= [all_movie_details[x].overview for x in range(len(all_movie_details))]


    #recommendation function
    
    
    embedding=prep(movie_details)
    
        
    listA=[]
    #turning the strings into word embeddings
    # embedding_many=[prepare(str(x)) for x in all_movie_detail]
    
    # import pickle
    # with open ('embedding_many.pickle', 'wb') as f:
    #     pickle.dump(embedding_many, f, 5)
    with open('/Users/jeffreyng/Movie_Recommender/embedding_many.pickle', 'rb') as f:
        embedding_many = pickle.load(f)
    
    #computing the dot product and cosine similarity
    for i in range(len(embedding_many)):
        listA.append(np.dot(embedding_many[i], embedding)/(np.linalg.norm(embedding_many[i])*np.linalg.norm(embedding)))
    

    df0= pd.Series(listA)
    df1= pd.Series([num for num in range(0,len(listA))])
    frames=[df0, df1]
    work= pd.concat(frames, axis=1)
    work['cos_sim']=listA
    #sorting the cosine similarities
    idx=work['cos_sim'].sort_values(ascending=False)[1:11].index 
        
    sorted_movies=[]
    for num in idx:
        values= work['cos_sim'][idx]
        sorted_movies.append(all_movie_details[num])
            
    
   
    return render_template('recommend.html', #s=s, all_movie_details=all_movie_details, 
                           movie_details=movie_details, sorted_movies=sorted_movies, values=values)