# Movie Geeks DB - using SpaCy word embeddings, I calculated the dot product and then the cosine similarity between the movies to make recommendations
Capstone 1 Project to Recommend Movies [deployed site](https://movie-recommender-mgdb2.onrender.com/) 

## Steps to run app:
FROM TERMINAL:
 * make sure you have dependencies installed, using "pip install -r requirements.txt"
 * "python3 seed.py" to load the database
 * "flask run" or "python3 app.py"

NOTE:
This repository contains some files that contain data from API that will be used in the database. Database contains 50,000+ movies. Recommender uses POS tagging and word embeddings of the tags to generate cosine similarities that will give us most similar movies. (Please refer to code for specific algorithm). 

In order for recommendation to work, please download en_core_web_lg model with:
python -m spacy download en_core_web_lg 

## FEATURES
This website allows users to look up their movies in a database by genre or my search and recommends movies to them. Features implemented include:
* a login/signup/logout feature to help users organize and browse movies 
* search feature to find user movies quickly
* movies separated by genre to allow users to browse if they don't have a movie in mind
* a favorites feature that allows users to mark the movie as favorite
* a watched feature that allows users to mark the movie as watched
* a recommendation system that recommends top 10 movie suggestions

## USERFLOW
The user flow starts with a sign up/login which requires a unique username and password. Upon signup a email is requested also. The user is welcomed to page and allowed to browse movies using app's search feature or browse by genre. Either option is robust in what the list returns especially of a user types an incomplete search, where app will include all movies with that search term. From there, the user can see the listed movies and select one for a detailed view. The detail view has the movies poster, popularity rating, synopsis, genre, and most importantly, a recommend button to recommend similar movies. In this page, there is also a favorite and watched button to allow users to save their likes/watches to database. The recommendation will lead to top 10 recommendations for the selected movie. The recos will have a synopsis and a user can select the reco movie for another detail view with same options and recommend that as well. Then finally, there is a log out.

The API is the tmdb [API](https://developer.themoviedb.org/docs/getting-started) using imdbcode to reach each movie's endpoint. Please use ipython and %run seed.py to seed the movie db into the app's database in order to get the app and recommendation running. 

## TECHNOLOGY STACK: 
* HTML5/ CSS
* Flask
* Javascript
* Jupyter Notebook for API calls
* Axios
* SpaCY
* Python3.9 which includes pandas, numpy, pickle

The app needs several downloads that may not be installed for the normal user:
    * SpaCY
    * en_core_web_lg
    * numpy and pandas
As stated above, en_core_web_lg can be installed using above code on command line and pip install spacy, pandas, numpy on the command line in a virtual environment should do the trick. Moreover the requirements.txt file has the environment to run this app on my machine. Although each computer may differ, calling a virtual environment and pip install -r requirements.txt should get these packages into your system.
