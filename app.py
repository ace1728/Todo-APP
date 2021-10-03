from re import A 
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests       #to send the request to the URL
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=(request.form['title'])
        desc=(request.form['desc'])
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        todo=Todo.query.filter_by(sno=sno).first()
        title=(request.form['title'])
        desc=(request.form['desc'])
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/gallery')
def gallery():
    url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
    #request allow you to send HTTP request
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    imgsource=[]
    images = soup.findAll('img',class_='loadlate')
    for image in images:
        imgsource.append(image['loadlate'])
    return render_template('gal.html',imgsource=imgsource)
    #return render_template('update.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather={}
    weather_data=[]
    if request.method == 'POST':
        new_city = request.form['city']
        if new_city:
           url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a5c44ceda13bf8992baf1972d3289219'
           r = requests.get(url.format(new_city)).json()
           weather = {
            'city' : r['name'],
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }        
        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data)

if __name__=="__main__":
    app.run(debug=True)