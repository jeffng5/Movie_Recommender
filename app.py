from flask import Flask, render_template, request, flash, redirect, session, g, sessions
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests, json
import json
import pandas as pd
# from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db, Movie, Tag
import pickle

app = Flask(__name__)
app.run(debug=True)
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql:///jeffreyng'
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"
# toolbar = DebugToolbarExtension(app)

api_key = '1288b79b'


connect_db(app)

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')



