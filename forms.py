from wtforms import DecimalField, StringField, SelectMultipleField, SelectField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, NumberRange, Length

class MovieForm(FlaskForm):
    title = StringField('movie title')



class CatalogForm(FlaskForm):
    genres= SelectField('genre', choices=[('Action', 'Action') ,
                                           ('Adventure', 'Adventure'), 
                                           ('Animation', 'Animation'), 
                                           ('Comedy', 'Comedy'), ('Crime', 'Crime' ),
                                           ('Documentary', 'Documentary'),     
('Drama','Drama'),           
('Family', 'Family'),         
('Fantasy','Fantasy'),        
('History','History'),         
('Horror', 'Horror'),          
('Music','Music'),           
('Mystery','Mystery'),         
('Romance' ,'Romance'),         
('Science Fiction','Science Fiction'), 
('TV Movie','TV Movie'),        
('Thriller' ,'Thriller'),        
('War','War'),
('Western', 'Western')])    


    # popularitys= DecimalField('popularity', validators=[NumberRange(min=0, max =50, message='testing')])
    # vote_averages= SelectField('vote_averages', choices= [(float(), '1-10'), (float(), '10-20'), (float(), '20-30'),(float(), '30-40', (float(), '40-50'))])

class UserAddForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password= PasswordField('password', validators=[InputRequired()])
    email= StringField('email')
    
class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

