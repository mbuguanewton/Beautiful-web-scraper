from bs4 import BeautifulSoup
from flask import Flask
from pymongo import MongoClient
import requests
from csv import writer
import time
import config

#app = Flask(__name__)


URI =  config.Mongo_URI
client = MongoClient(URI, connectTimeoutMS = 30000)
db = client.get_database('movie-data')

#mongo = PyMongo(app)


start = time.time()

for i in range(1,1000):
  i+=1
  # enter the url of the website you want to scrap
  response = requests.get('https://www.themoviedb.org/tv?page='+ str(i))
  soup = BeautifulSoup(response.text, 'html.parser')
  posts = soup.find_all(class_ = 'item poster card')


  # function / method to write to a csv file
  #with open('movies.csv', 'w', encoding='utf-8') as csv_file:
    #csv_writer = writer(csv_file)
    #headers = ['Movie Title','Movie Synopsis','Movie Image','Release Date','Score']
    #csv_writer.writerow(headers)

  #connect to mongodb  
  movies = db.movies_collections
  for post in posts:
    # scrap the movie title
    MovieTitle = post.find(class_ = 'title result').get_text()
    # scrap the synopsis or description
    MovieSynopsis = post.find(class_='overview').get_text().replace('\n', '')
    # scrap the poster image
    try:
      MovieImage = post.find('img')['data-src']
    except TypeError:
      MovieImage = "https://images.pexels.com/photos/274937/pexels-photo-274937.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
    # scrap the movie release date
    ReleaseDate = post.find(class_='flex').find('span').get_text()
    # scrap the score of the movie
    Score = post.find(class_ = 'user_score_chart')['data-percent']

    # create row with a list of all the movie attributes
    movies.insert_one({'Movie Title': MovieTitle,'Movie Synopsis': MovieSynopsis, 'Movie Image': MovieImage, 'Release Date':ReleaseDate, 'Score': Score})
  
end = time.time()

print({"Start time":start, "End time":end})


      

