import pickle
from sqlalchemy.orm import Session
from models import Movie,db
from app import db

db.drop_all()
db.create_all()

with open('mvtitles.pickle', 'rb') as f:
    moviedb = pickle.load(f)



stuff= Movie(
                 title = moviedb[0]['movie_results'][0]['title'],
                image = moviedb[0]['movie_results'][0]['poster_path'],
                 genre1= moviedb[0]['movie_results'][0]['genre_ids'][0],
                 genre2= moviedb[0]['movie_results'][0]['genre_ids'][1],
                #  genre3 = moviedb[0]['movie_results'][0]['genre_ids'][2],
                 overview=moviedb[0]['movie_results'][0]['overview'],
                #  release_year= (moviedb[0]['movie_results'][0]['release_date']),
                 popularity=moviedb[0]['movie_results'][0]['popularity'],
                 vote_average=moviedb[0]['movie_results'][0]['vote_average']
                 )
db.session.rollback()
db.session.add_all([stuff])
db.session.commit()