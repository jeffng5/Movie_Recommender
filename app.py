from flask import Flask, render_template, request, flash, redirect, session, jsonify, g, abort
# from flask_session import Session
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import func
import requests, json
import json
import pickle
from collections.abc import Mapping
import pandas as pd
from forms import MovieForm, CatalogForm, UserAddForm, LoginForm
from models import db, connect_db, Movie, Tag, User, Favorite, Watched
import spacy
import numpy as np

        
app = Flask(__name__)
# app.app_context().push()
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://norylmst:9otnRav6eugshKTmGTSo1Xf_iVLV4ZN3@mahmud.db.elephantsql.com/norylmst'
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
        email=form.email.data
        
        for ele in User.query.all():
            if ele.username == username:
                return redirect("/signup")
        
        user=User.register(username, password, email)
        db.session.add(user)

        db.session.commit()
        
        
            
        session["user_id"] = user.id
        if user.id:
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
            session['user_id'] = u.id
            return redirect("/intro")

        else:
            return (f'IT DIDNT WORK!!')
            
    return render_template('login.html', form=form)

@app.route('/intro', methods=['GET', 'POST'])
def intro():
    print(session['user_id'])
    try:
        if session['user_id']:
            identify = User.query.filter_by(id=session['user_id']).first()
            return render_template('intro.html', identify=identify)
    except: 
        return redirect("/login")   
       


@app.route('/search', methods=['GET','POST'])
def search_movie():
   

    form = MovieForm()
    if form.validate_on_submit():
        
        watched_movies = Movie.query.filter(Movie.id==Watched.movie_id, Watched.user_id==session['user_id']).all()
        favorited_movies = Movie.query.filter(Movie.id==Favorite.movie_id, Watched.user_id==session['user_id']).all()
        term = form.title.data
        try:
            list_of_movies = Movie.query.filter(Movie.title.ilike("%" + term + "%")).order_by(Movie.popularity.desc())
        except: 
            len(list_of_movies)==0
            return render_template('error.html')
        u_id= session['user_id']

        
        # favorite= Favorite(user_id=u_id, movie_id=m_id)
        # db.session.add(favorite)
        # db.session.commit()
    
        return render_template("select.html", list_of_movies= list_of_movies, favorited_movies= favorited_movies, watched_movies= watched_movies)
    else:
        return render_template("search.html", form = form) 




@app.route('/catalog', methods=['GET', 'POST'])
def browse():

    form = CatalogForm()
    if form.validate_on_submit():
        genres = form.genres.data
        list_of_movies_by_genres = Movie.query.filter_by(genre1 = genres).order_by(Movie.popularity.desc())
        list_of_movies_by_genres1 = Movie.query.filter(Movie.genre2 == genres).order_by(Movie.popularity.desc())
        
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
    if type(id) != int():
        flash("the url must be a valid integer")
    user_id = session['user_id']
    movie_details= Movie.query.filter(Movie.id==id)
    return render_template('movie_details.html', movie_details=movie_details)
    if Favorite.query.filter(Favorite.movie_id==id, Favorite.user_id==user_id) :
        movie_details = Movie.query.filter(Movie.id==id, Favorite.user_id==user_id)
        return render_template('movie_details_liked.html', movie_details=movie_details)
    

@app.route('/logout')
def logout():
    """Handle logout of user."""
    session.pop('user_id')
    flash(f'LOGOUT SUCCESSFUL!!')
    return render_template('home.html')


nlp= spacy.load("en_core_web_lg")
spacy_tokenizer=nlp.tokenizer


def prep(x):
    embedding=nlp(x).vector.reshape(300,)
    return embedding
    
def prepare(x):
    embedding_many=nlp(x).vector.reshape(300,)
    return embedding_many

@app.route('/recommendation/<int:id>')
def recommend_movie(id):
    movie_details= Movie.query.filter(Movie.id==id).first()
    # movie_details= [movie_details[x].overview for x in range(len(movie_details))]
    all_movie_details= Movie.query.all()
    
    total_movie_details=list(all_movie_details[14000:])
    movie_details= movie_details.overview
    # total = [total_movie_details[x].overview for x in range(0,len(total_movie_details))]
    

    
    
    
    embedding=prep(movie_details)
    
        
    listA=[]
    # turning the strings into word embeddings
    # embedding_many=[]
    # for x in total:
    #     try:
    #         embedding_many.append(prepare(x))
    #     except:
    #         pass

    
    
    #opening the file
    with open('./embedding_many.pickle', 'rb') as f:
        embedding_many = pickle.load(f)
    
    
    # pickling the file
    # with open ('embedding_many.pickle', 'wb') as f:
    #     pickle.dump(embedding_many, f, 5)

    #computing the dot product and cosine similarity
  
    for i in range(len(embedding_many)):
        listA.append(np.dot(embedding_many[i], embedding)/(np.sqrt(np.sum(np.square(embedding_many[i])))*np.sqrt(np.sum(np.square(embedding)))))
    

    df0= pd.Series(listA)
    df1= pd.Series([num for num in range(0,len(listA))])
    frames=[df1, df0]
    work= pd.concat(frames, axis=1)
    work['cos_sim']=listA
    #sorting the cosine similarities
    idx=work['cos_sim'].sort_values(ascending=False)[1:11].index 
    values= work['cos_sim'][idx]

    sorted_movies=[]
    for num in idx:
        sorted_movies.append(total_movie_details[num])
    
   
    return render_template('recommend.html', sorted_movies=sorted_movies, values=values, idx=idx)
                        #    movie_details=movie_details, sorted_movies=sorted_movies, values=values)


@app.route('/post-to-favorites', methods=['POST'])
def add_favorite():
    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")

    id=session['user_id']
    data = request.get_json(force=True)
    item0 = data['movie_id']
    # item1 = data.get('image1')
    if item0:
        user_id= id
        movie_id = item0
        record=Favorite(user_id=user_id, movie_id=movie_id)
        db.session.add(record)
        db.session.commit()
    # elif item1:
    #      user_id= session['user_id']
    #      movie_id = item0
    #      x = Favorite.query.filter(Favorite.user_id==user_id, Favorite.movie_id==movie_id)
    #      db.session.delete(x)
    #      db.session.commit()
    return render_template("movie_details.html", m_id =item0) 


@app.route('/post-to-unfavorites', methods=['POST'])
def unfavorite_movie():
    data = request.get_json(force=True)
    item = data['movie_id']

    if item:
        user_id= session['user_id']
        movie_id = item
        Favorite.query.filter(Favorite.movie_id == movie_id, Favorite.user_id == user_id).delete()
        db.session.commit()

    return render_template("movie_details.html", item=item )


@app.route("/post-to-unwatched", methods=['POST'])
def unwatch_movie():
    data = request.get_json(force=True)
    item = data['movie_id']

    if item:
        user_id = session['user_id']
        movie_id=item
        print(item)
        Favorite.query.filter(Favorite.movie_id==movie_id , Favorite.user_id==user_id).delete()
        db.session.commit()
    
    return render_template("movie_details.html")

@app.route("/post-to-watched", methods=['POST'])
def watch_movie():
    data = request.get_json(force=True)
   
    item = data['movie_id']
    print(item)
    if item:
        user_id = session['user_id']
        movie_w = item
        
        watched_movie=Watched(user_id = user_id, movie_id = movie_w)
        db.session.add(watched_movie)
        db.session.commit()
    
    return render_template('movie_details.html')


@app.route('/favorited-watched')
def get_favorited():
    
    data=request.get_json(force=True)
    item= data['movie_id']
    
    
    # watched = Movie.query.filter(Watched.movie_id==id, User.watched_movies.id ==session['user_id'])
    return render_template('favorited-watched.html') 
    
    
   
# @app.route('/get-rid-of-watched', methods=['POST'])
# def delete_from_watched_list():
#     data = request.get_json(force=True)
#     item = data['movie_id']

#     if item:
#         user_id = session['user_id']
#         movie_id=item
#         print(item)
#         Watched.query.filter(Watched.movie_id == movie_id, Watched.user_id == user_id).delete()
#         db.session.commit()
    
#     return render_template("favorited-watched.html")






# @app.route('/get-rid-of-favorites', methods=['POST'])
# def delete_from_favorite_list():
#     data = request.get_json(force=True)
#     item = data['movie_id']
#     print(item)
#     if item:
#         user_id= session['user_id']
#         movie_id = item
#         show = db.session.query(Movie.id, Favorite.movie_id, Favorite.user_id).join(Favorite).all()
#         # print(show.query.filter(Favorite.user_id==user_id, Favorite.movie_id==item).delete())
#         print(show)
        
#         Favorite.query.filter(Favorite.movie_id == movie_id, Favorite.user_id == user_id).delete()
#         db.session.commit()

#     return render_template("favorited-watched.html")


