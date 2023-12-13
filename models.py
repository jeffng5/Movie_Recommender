from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, bcrypt
from sqlalchemy import Float


bcrypt=Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Favorite(db.Model):

    __tablename__ = 'favorites'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)


    movie_f = db.relationship('Movie', cascade="all,delete", backref= 'favorites')
    favorite = db.relationship("User", cascade="all,delete", backref="favorites")

class Watched(db.Model):

    __tablename__= 'watcheds'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)


    movie_w = db.relationship('Movie', cascade="all,delete", backref= 'watcheds')
    watched = db.relationship('User', cascade='all,delete', backref= 'watcheds')

class Movie(db.Model):

    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    image= db.Column(db.String, nullable=True)
    genre1= db.Column(db.String, nullable=False)
    genre2= db.Column(db.String, nullable=True)
    summary=db.Column(db.Text, nullable=False)
    overview = db.Column(db.Text, nullable=False)
    popularity = db.Column(db.Float(precision=5), nullable=True)
    
    favorite_movies= db.relationship('Favorite', cascade= "all,delete", backref= 'movies')
    watched_movies=db.relationship('Watched', cascade='all,delete', backref= 'movies')

class Tag(db.Model):

    __tablename__ = 'tags'
    
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    movie_id= db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    tag = db.Column(db.String, nullable=False)

    movies= db.relationship('Movie', cascade='all,delete', backref='tags')
    
class User(db.Model):

    __tablename__ = 'users'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username= db.Column(db.Text, unique=True, nullable=False)
    password=db.Column(db.Text, nullable=False)
    email= db.Column(db.String, nullable=True)

    join= db.relationship('Movie', secondary='favorites', backref= 'fav_movie_by_user')
    join1= db.relationship('Movie', secondary = 'watcheds', backref= 'watched_movie_by_user')
    
    # start_register
    @classmethod
    def register(cls, username, pwd, email):
        """Register user w/hashed password & return user."""
        # password= password.encode('utf-8')
        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        
        return cls(username=username, password=hashed_utf8, email=email)

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

   






    