import spacy
import numpy as np
from unittest import TestCase
import pandas as pd
import pickle

nlp= spacy.load("en_core_web_lg")
spacy_tokenizer=nlp.tokenizer
def prep(x):
    embedding=nlp(x).vector.reshape(300,)
    return embedding
def test_answer():

    assert len(prep("Good morning")== 300) 



def recommend_movie():
    with open('/Users/jeffreyng/Movie_Recommender/embedding_many.pickle', 'rb') as f:
        embedding_many = pickle.load(f)
        return embedding_many 
def test_answer():
    with open('/Users/jeffreyng/Movie_Recommender/embedding_many.pickle', 'rb') as f:
        embedding_many = pickle.load(f)
    assert len(embedding_many) == 42519 


