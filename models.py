from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Movie(db.Model)
    
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    actor1 = db.Column(db.String, nullable=False)
    actor2 = db.Column(db.String, nullable=False)
    actor3 = db.Column(db.String, nullable=False)
    genre1= db.Column(db.String, nullable=False)
    genre2= db.Column(db.String, nullable=True)
    director= db.Column(db.String, nullable=False)
    plot = db.Column(db.Text, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    released = db.Column(db.Intger, nullable=True)
    imdb_rating = db.Column(db.String, nullable=False)
    poster = db.Column(db.String, nullable=True)



class Tag(db.Model)

    __tablename__ = 'tags'
    
    movie_id= db.Column(db.Integer, ForeignKey= Movie.id, nullable=False)
    tag = db.Column(db.String, nullable=False)
    