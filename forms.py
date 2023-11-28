from wtforms import SelectField, StringField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class MovieForm(FlaskForm):
    title = StringField('movie title')



class CatalogForm(FlaskForm):
    title = StringField('movie title')
    genres= StringField('genre')
    # popularitys= SelectField('popularity', choices= [(float(), '1-5')])
    # vote_averages= SelectField('vote_averages', choices= [(6, 7)])


class UserAddForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password= PasswordField('password', validators=[InputRequired()])
    email= StringField('email')
    
class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
