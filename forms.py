from wtforms import DecimalField, StringField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, NumberRange, Length

class MovieForm(FlaskForm):
    title = StringField('movie title')



class CatalogForm(FlaskForm):
    genres= StringField('genre')
    # popularitys= DecimalField('popularity', validators=[NumberRange(min=0, max =50, message='testing')])
    # vote_averages= SelectField('vote_averages', choices= [(float(), '1-10'), (float(), '10-20'), (float(), '20-30'),(float(), '30-40', (float(), '40-50'))])

class UserAddForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password= PasswordField('password', validators=[InputRequired()])
    email= StringField('email')
    
class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
