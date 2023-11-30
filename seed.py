import pickle
from flask import Flask
from sqlalchemy.orm import Session
from models import Movie, db, Tag, User, Favorite, Watched, Embedding
from app import db, prepare
from sqlalchemy import MetaData
from sqlalchemy import create_engine

import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)

def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)
register_adapter(np.int32, addapt_numpy_int32)
register_adapter(np.ndarray, addapt_numpy_array)

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
    
import spacy
import numpy as np
nlp= spacy.load("en_core_web_lg")
spacy_tokenizer=nlp.tokenizer
import pandas as pd

def prepare(x):
    # tokenizing=spacy_tokenizer(x)
    embedding_many=nlp(x).vector.reshape(30,10)
    return embedding_many

# all_movie_details= Movie.query.all()
# movie_details=all_movie_details.overview
# all_movie_detail= [all_movie_details[x].overview for x in range(len(all_movie_details))]

# embedding_many=[prepare(str(x)) for x in subj]

# for i in range(len(embedding_many)):
#     stuff = Embedding(
#         embedding=embedding_many[i]
#     )
#     db.session.add(stuff)




db.session.commit()