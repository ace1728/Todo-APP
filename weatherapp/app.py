from os import name
import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather={}
    weather_data=[]
    if request.method == 'POST':
        new_city = request.form['city']
        if new_city:
           wet=City(name=new_city)
           db.session.add(wet)
           db.session.commit()
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