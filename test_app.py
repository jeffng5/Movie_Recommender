import spacy
import numpy as np
from unittest import TestCase
import pytest
import pandas as pd
import pickle
from flask import session, Flask
from models import connectdb, db

nlp= spacy.load("en_core_web_lg")
spacy_tokenizer=nlp.tokenizer


app = Flask(__name__)
connect_db(app)
app.app_context().push()
# app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']




class FunctionsTestCase(TestCase):

# testing that an input results in a 300 dimensional vector
    def test_answer(self):
        # defining prep function
        def prep(x):
            embedding=nlp(x).vector.reshape(300,)
            return embedding
        assert len(prep("Good morning")== 300)
        
        def prepare(x):
            embedding = nlp(x).vector.reshape(300,)
            return embedding
        assert len(prepare('Hello')== 300) 


# testing that the pickled object loads
    def test_recommend_movie(self):
        with open('/Users/jeffreyng/Movie_Recommender/embedding_many.pickle', 'rb') as f:
            embedding_many = pickle.load(f)
            self.assertIsNotNone(embedding_many) 

#testing the size of pickled object is correct
    def test_length_of_object(self):
        with open('/Users/jeffreyng/Movie_Recommender/embedding_many.pickle', 'rb') as f:
            embedding_many = pickle.load(f)
        assert len(embedding_many) == 42519 
        



class RoutesTestCase(TestCase): 

    
    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<title>Movie Recommender</title>', html)

    def test_signup(self):
        with app.test_client() as client:
            res = client.get('/signup')
            self.assertEqual(res.status_code, 200)
            
            html = res.get_data(as_text=True)
            self.assertIn('<h2>Register</h2>', html)
    
    def test_login(self):
        with app.test_client() as client:
            res = client.get('/login')
            self.assertEqual(res.status_code, 200)
            
            html = res.get_data(as_text=True)
            self.assertIn('<title>Movie Recommender</title>', html)    
 
    
    def test_search(self):
        with app.test_client() as client:
            res = client.get('/search')
            self.assertEqual(res.status_code, 200)
            
            html = res.get_data(as_text=True)
            self.assertIn('<h3>Search for Movie</h3>', html)   
    
    def test_catalog(self):
        with app.test_client() as client:
            res = client.get('/catalog')
            self.assertEqual(res.status_code, 200)
            
            html = res.get_data(as_text=True)
            self.assertIn('<title>Movie Recommender</title>', html)   
    
    def test_logout(self):
        with app.test_client() as client:
            res = client.get('/logout')
            self.assertEqual(res.status_code, 200)

    def test_post_to_favorites(self):
        with app.test_client() as client:
            res = client.post('/post-to-favorites')
            self.assertEqual(res.status_code, 201)
            
    def test_post_to_watched(self):
        with app.test_client() as client:
            res = client.post('/post-to-watched')
            self.assertEqual(res.status_code, 201)
    
    def test_favorited_watched(self):
        with app.test_client() as client:
            res = client.get('/favorite-watched')
            self.assertEqual(res.status_code, 200)