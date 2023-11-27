from wtforms import SelectField, StringField
from flask_wtf import FlaskForm

class MovieForm(FlaskForm):
    title = StringField('movie title')



class BrowseForm(FlaskForm):
    title = StringField('movie title')
    genres= StringField('genre')
    popularitys= SelectField('popularity')
    vote_averages= SelectField('vote_averages')