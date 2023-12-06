# Movie_Recommender 
Capstone 1 project to recommend movies 

NOTE:
This repository contains some files that contain data from API that will be used in the database. Database contains 50,000+ movies. Recommender uses POS tagging and word embeddings of the  tags to generate cosine similarities that will give us most similar movies. (Please refer to code for specific algorithm). 

In order for recommendation to work, please download en_core_web_lg model with:
python -m spacy download en_core_web_lg 
