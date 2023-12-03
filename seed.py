import pickle
from flask import Flask
from sqlalchemy.orm import Session
from models import Movie, db, Tag, User, Favorite, Watched
from app import db, prepare
from sqlalchemy import MetaData, Table, Column, Numeric, Integer, VARCHAR
from sqlalchemy import create_engine
from sqlalchemy import text


# metadata=MetaData()
#engine = create_engine('postgresql:///jeffreyng')
#meta = MetaData(bind=engine)
# MetaData.reflect(meta)
#meta.create_all()

# Movie.__table__.drop(engine)

# db.session.rollback()
db.drop_all()
# db.session.rollback()
db.create_all()
db.session.commit()




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
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/subj.pickle', 'rb') as f:
    subj = pickle.load(f)
with open('/Users/jeffreyng/Movie_Recommender/static/pickle/synopsis.pickle', 'rb') as f:
    synopsis = pickle.load(f)







for i in range(len(name)):
    stuff= Movie(
                   title = name[i],
                    image = images[i],
                    genre1= genres1[i],
                    genre2= genres2[i],
                    summary= synopsis[i],
                    overview=subj[i],
                    popularity=popularitys[i],
                    vote_average= popularitys[i]
                 )

    db.session.add(stuff)
for i in range(1, len(subj)):
    tags = Tag(
        movie_id= i,
        tag = subj[i]
    )
    db.session.add(tags)
    

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