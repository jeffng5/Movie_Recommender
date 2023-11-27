from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Movie(db.Model):

    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    image= db.Column(db.String, nullable=True)
    genre1= db.Column(db.String, nullable=False)
    genre2= db.Column(db.String, nullable=True)
    genre3= db.Column(db.String, nullable=True)
    overview = db.Column(db.Text, nullable=False)
    # release_year = db.Column(db.String, nullable=True)
    popularity = db.Column(db.String, nullable=False)
    vote_average = db.Column(db.String, nullable=True)



class Tag(db.Model):

    __tablename__ = 'tags'
    
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    movie_id= db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    tag = db.Column(db.String, nullable=False)

    movies= db.relationship('Movie', backref='tags')
    
class User(db.Model):

    __tablename__ = 'users'

    id=db.Column(db.Integer, primary_key= True, autoincrement=True, nullable=False)
    username= db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    firstname= db.Columnn(db.String, nullable=False)
    lastname= db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False)
    location= db.Column(db.String, nullable=True)

class Favorite(db.Model):

    __tablename__ = 'favorites'

    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    title= db.Column(db.String, db.ForeignKey('movies.title'), nullable=False)

    favorite = db.relationship('Movie', backref= 'favorites')
    favorited_user = db.relationship('User', backref= 'favorites')

class Watched(db.Model):

    __tablename__= 'watcheds'

    user_id= db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    title=db.Column(db.String, db.ForeignKey('movies.title'), nullable=False)

    watched = db.relationship('Movie', backref= 'watcheds')
    watched_user = db.relationship('User', backref= 'watcheds')