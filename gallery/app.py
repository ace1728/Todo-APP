from re import A 
from flask import Flask, render_template, request, redirect
#importing required Libraries
import pandas as pd   #to create dataframe
import requests       #to send the request to the URL
from bs4 import BeautifulSoup #to get the content in the form of HTML
import numpy as np  # to count the values (in our case)

app = Flask(__name__)





@app.route('/')
def hello_world():
    url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
    #request allow you to send HTTP request
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    imgsource=[]
    images = soup.findAll('img',class_='loadlate')
    for image in images:
        imgsource.append(image['loadlate'])
    return render_template('gal.html',imgsource=imgsource)

if __name__=="__main__":
    app.run(debug=True)