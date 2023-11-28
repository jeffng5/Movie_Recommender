from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, bcrypt
bcrypt=Bcrypt()
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
    # popularity = db.Column(db.Float(precision=2), nullable=False)
    # vote_average = db.Column(db.Float(precision=2), nullable=False)



class Tag(db.Model):

    __tablename__ = 'tags'
    
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    movie_id= db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    tag = db.Column(db.String, nullable=False)

    movies= db.relationship('Movie', backref='tags')
    
class User(db.Model):

    __tablename__ = 'users'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    username= db.Column(db.Text, unique=True, nullable=False)
    password=db.Column(db.Text, nullable=False)
    email= db.Column(db.String, nullable=True)


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

   

class Favorite(db.Model):

    __tablename__ = 'favorites'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id= db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    title= db.Column(db.String, nullable=False)

    # favorite = db.relationship('User', backref= 'favorites')
    

class Watched(db.Model):

    __tablename__= 'watcheds'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id= db.Column(db.Integer,nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    title=db.Column(db.String, nullable=False)

    # watched = db.relationship('User', backref= 'watcheds')
    