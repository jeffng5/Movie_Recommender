from flask import Flask, render_template, request, flash, redirect, session, jsonify, g, abort, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from flask_executor import Executor
import spacy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import desc, create_engine
from sqlalchemy.sql import func
import requests, json
import pickle
import pandas as pd
from forms import MovieForm, CatalogForm, UserAddForm, LoginForm
from models import db, connect_db, Movie, Tag, User, Favorite, Watched
import numpy as np
import os
from werkzeug.urls import url_encode


        
app = Flask(__name__)
executor = Executor(app)
# db.create_all()
# app.app_context().push()
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("URL1")
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SECRET_KEY'] = "it's a secret"


connect_db(app)
#opening the file
with open('./embedding_many.pickle', 'rb') as f:
    embedding_many = pickle.load(f)

progress = {"percent": 0, "running": False, "error": None}
recommendation_cache = {}

SEARCH_RESULTS_PER_PAGE = 60
CATALOG_RESULTS_PER_PAGE = 60
SESSION_SEARCH_TITLE_KEY = "search_movie_title"
SESSION_CATALOG_GENRE_KEY = "catalog_genre"

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
    page = request.args.get('page', 1, type=int) or 1
    if page < 1:
        page = 1

    if form.validate_on_submit():
        session[SESSION_SEARCH_TITLE_KEY] = (form.title.data or "").strip()
        return redirect(url_for('search_movie', page=1))

    if request.method == 'GET' and request.args.get('page') is None:
        session.pop(SESSION_SEARCH_TITLE_KEY, None)
        return render_template("search.html", form=form)

    term = session.get(SESSION_SEARCH_TITLE_KEY) or ""
    if not term:
        return render_template("search.html", form=form)

    watched_movies = Movie.query.filter(
        Movie.id == Watched.movie_id, Watched.user_id == session['user_id']
    ).all()
    favorited_movies = Movie.query.filter(
        Movie.id == Favorite.movie_id, Watched.user_id == session['user_id']
    ).all()

    query = Movie.query.filter(
        Movie.title.ilike("%" + term + "%"),
        Movie.image.isnot(None),
        Movie.image != "",
    ).order_by(Movie.popularity.desc())
    pagination = query.paginate(
        page=page, per_page=SEARCH_RESULTS_PER_PAGE, error_out=False
    )
    if pagination.total == 0:
        return render_template("error.html")

    return render_template(
        "select.html",
        list_of_movies=pagination.items,
        pagination=pagination,
        favorited_movies=favorited_movies,
        watched_movies=watched_movies,
    )




@app.route('/catalog', methods=['GET', 'POST'])
def browse():
    form = CatalogForm()
    page = request.args.get('page', 1, type=int) or 1
    if page < 1:
        page = 1

    if request.method == 'POST' and form.validate_on_submit():
        session[SESSION_CATALOG_GENRE_KEY] = form.genres.data
        return redirect(url_for('browse', page=1))

    if request.method == 'GET' and request.args.get('page') is None:
        session.pop(SESSION_CATALOG_GENRE_KEY, None)
        return render_template('catalog.html', form=form)

    genre = session.get(SESSION_CATALOG_GENRE_KEY)
    if not genre:
        return render_template('catalog.html', form=form)

    uid = session.get('user_id')
    if uid:
        watched_movies = Movie.query.filter(
            Movie.id == Watched.movie_id, Watched.user_id == uid
        ).all()
        favorited_movies = Movie.query.filter(
            Movie.id == Favorite.movie_id, Favorite.user_id == uid
        ).all()
    else:
        watched_movies = []
        favorited_movies = []

    query = Movie.query.filter_by(genre1=genre).order_by(Movie.popularity.desc())
    pagination = query.paginate(
        page=page, per_page=CATALOG_RESULTS_PER_PAGE, error_out=False
    )
    if pagination.total == 0:
        return render_template('error.html')

    return render_template(
        'last_page.html',
        list_of_movies=pagination.items,
        pagination=pagination,
        genre=genre,
        favorited_movies=favorited_movies,
        watched_movies=watched_movies,
    )

# Movie.query.filter(Movie.title.ilike("%" + term + "%")).all()
#    left inner join
# Favorites.movie.filter_by(Favorites.user_id = User.id)


@app.route("/<int:id>", methods=['POST', 'GET'])
def single_movie(id):
    if type(id) != int():
        flash("the url must be a valid integer")
    user_id = session['user_id']

    if request.method == 'POST':
        
        data = request.get_json()
        print(data.get('title'))
        title = data.get('title')
        movie_title = {
            'title' : title
        }
        
        movie_details= Movie.query.filter(Movie.title==title).first()
        print(movie_details)
        record = Favorite(user_id=user_id, movie_id=id)
    
        db.session.add(record)
        db.session.commit()
        return jsonify(movie_title)

    if request.method == 'GET':
        movie_details= Movie.query.filter(Movie.id==id)
        return render_template('movie_details.html', movie_details=movie_details)
    # if Favorite.query.filter(Favorite.movie_id==id, Favorite.user_id==user_id) :
    #     movie_details = Movie.query.filter(Movie.id==id, Favorite.user_id==user_id)
    #     return render_template('movie_details_liked.html', movie_details=movie_details)
    

@app.route('/logout')
def logout():
    """Handle logout of user."""
    session.clear()
    flash(f'LOGOUT SUCCESSFUL!!')
    return render_template('home.html')


# spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")
spacy_tokenizer=nlp.tokenizer


def prep(x):
    embedding=nlp(x).vector.reshape(300,)
    return embedding
    
def prepare(x):
    embedding_many=nlp(x).vector.reshape(300,)
    return embedding_many


def _compute_sorted_recommendations(movie_id, on_progress=None):
    """Cosine-similarity pipeline. Optional on_progress(percent) updates 0–100."""
    film = Movie.query.filter(Movie.id == movie_id).first()
    if not film:
        raise ValueError("Movie not found")

    def bump(p):
        if on_progress:
            on_progress(min(100, int(p)))

    all_movie_details = Movie.query.all()
    total_movie_details = list(all_movie_details[14000:])
    overview_text = film.overview
    bump(2)

    embedding = prep(overview_text)
    bump(6)

    slice_emb = embedding_many[14000:]
    total = len(slice_emb)
    listA = []
    if total == 0:
        bump(100)
        return film, []

    report_every = max(1, total // 80)
    for i in range(total):
        row = slice_emb[i]
        listA.append(
            np.dot(row, embedding)
            / (
                np.sqrt(np.sum(np.square(row)))
                * np.sqrt(np.sum(np.square(embedding)))
            )
        )
        if on_progress and (i % report_every == 0 or i == total - 1):
            bump(6 + (90 * (i + 1) / total))

    bump(93)
    df0 = pd.Series(listA)
    df1 = pd.Series([num for num in range(0, len(listA))])
    frames = [df1, df0]
    work = pd.concat(frames, axis=1)
    work["cos_sim"] = listA
    idx = work["cos_sim"].sort_values(ascending=False)[1:11].index

    sorted_movies = []
    for num in idx:
        sorted_movies.append(total_movie_details[num])

    bump(100)
    return film, sorted_movies


def recommend_job(app, movie_id):
    global progress, recommendation_cache
    with app.app_context():
        try:
            progress.clear()
            progress.update({"percent": 0, "running": True, "error": None})

            def bump(p):
                progress["percent"] = min(100, int(p))

            film, sorted_movies = _compute_sorted_recommendations(movie_id, bump)
            recommendation_cache[movie_id] = {
                "film_id": film.id,
                "sorted_ids": [m.id for m in sorted_movies],
            }
            progress["percent"] = 100
            progress["running"] = False
        except Exception as e:
            progress["running"] = False
            progress["error"] = str(e)
            progress["percent"] = 0


@app.route("/recommendation/start/<int:movie_id>", methods=["POST"])
def start_recommendation(movie_id):
    if progress.get("running"):
        return jsonify({"error": "Recommendation already in progress"}), 409
    executor.submit(recommend_job, app, movie_id)
    return jsonify({"started": True})


@app.route('/recommendation/<int:id>')
def recommend_movie(id):
    cached = recommendation_cache.pop(id, None)
    if cached:
        film = Movie.query.filter(Movie.id == cached["film_id"]).first()
        ids = cached["sorted_ids"]
        if not film:
            return render_template("error.html")
        if not ids:
            sorted_movies = []
        else:
            by_id = {m.id: m for m in Movie.query.filter(Movie.id.in_(ids)).all()}
            sorted_movies = [by_id[i] for i in ids if i in by_id]
        return render_template("recommend.html", film=film, sorted_movies=sorted_movies)

    film, sorted_movies = _compute_sorted_recommendations(id, on_progress=None)
    return render_template("recommend.html", film=film, sorted_movies=sorted_movies)
                    


@app.route('/post-to-favorites', methods=['GET','POST'])
def add_favorite():
    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")

    id=session['user_id']
    data = request.get_json(force=True)
    item0 = data['movie_id']
    item1 = data['title']
    # item1 = data.get('image1')
    if item0:
        user_id= id
        movie_id = item0
        movie = item1
        record=Favorite(user_id=user_id, movie_id=movie_id, title= title)
        db.session.add(record)
        db.session.commit()
    # elif item1:
    #      user_id= session['user_id']
    #      movie_id = item0
    #      x = Favorite.query.filter(Favorite.user_id==user_id, Favorite.movie_id==movie_id)
    #      db.session.delete(x)
    #      db.session.commit()
    return render_template("movie_details.html", m_id =item0) 

@app.route("/post-to-watched", methods=['GET','POST'])
def watch_movie():
    
    user_id = session['user_id']
    if request.method == 'POST':
        
        data = request.get_json()
        print(data.get('movie_id'))
        id = data.get('movie_id')
        movie_id = {
            'movie_id' : id
        }
   
        record = Watched(user_id=user_id, movie_id=id)
    
        db.session.add(record)
        db.session.commit()
        return jsonify()

@app.route('/favorited-watched')
def get_favorited():
    u_id = session['user_id']
    engine = create_engine(os.environ.get("URL1"))
    with engine.connect() as connection:
        result = connection.execute('SELECT DISTINCT movies.id, movies.title, movies.image, favorites.user_id FROM favorites INNER JOIN movies ON movies.id = favorites.movie_id WHERE favorites.user_id = {}'.format(u_id))
        
    
    with engine.connect() as connection:
        watched = connection.execute('SELECT DISTINCT movies.id, movies.title, movies.image, watcheds.user_id from watcheds INNER JOIN movies ON movies.id = watcheds.movie_id WHERE user_id = {}'.format(u_id))
        print(watched)
    return render_template('favorited-watched.html', result = result, watched= watched) 
    


@app.route("/progress")
def get_progress():
    return jsonify(
        {
            "percent": progress.get("percent", 0),
            "running": progress.get("running", False),
            "error": progress.get("error"),
        }
    )



