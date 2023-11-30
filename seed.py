import pickle
from flask import Flask
from sqlalchemy.orm import Session
from models import Movie, db, Tag, User, Favorite, Watched
from app import db
from sqlalchemy import MetaData
from sqlalchemy import create_engine

# metadata=MetaData()
# engine = create_engine('postgresql:///jeffreyng')
# metadata.bind = engine
# meta.create_all(engine)

db.session.rollback()
db.create_all()

with open('/Users/jeffreyng/Movie_Recommender/static/pickle/name.pickle', 'rb') as f:
    name = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/images.pickle', 'rb') as f:
    images = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/genres1.pickle', 'rb') as f:
    genres1 = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/genres2.pickle', 'rb') as f:
    genres2 = pickle.load(f)
# with open('/Users/jeffreyng/Movie_Recommender/release_years.pickle', 'rb') as f:
#     release_years = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/popularitys.pickle', 'rb') as f:
    popularitys = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/vote_averages.pickle', 'rb') as f:
    vote_averages = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/subj.pickle', 'rb') as f:
    subj = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/topic.pickle', 'rb') as f:
    topicz = pickle.load(f)
for i in range(len(name)):
    stuff= Movie(
                 title = name[i],
                 image = images[i],
                 genre1= genres1[i],
                 genre2= genres2[i],
                 summary= topicz[i],
                 overview=subj[i],
                #  release_year= release_years[i],
                 popularity=popularitys[i],
                 vote_average=vote_averages[i]
                 )

    db.session.add(stuff)
for i in range(1,len(subj)):
    tags = Tag(
        movie_id= i,
        tag = subj[i]
    )
    db.session.add(tags)








db.session.commit()