import requests
import string
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)


class city(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=1b7327427012cd35c4de782378022165"
    r = requests.get(url).json()
    return r

@app.route('/')
def index_get():
    cities = city.query.all()

    weather_data = []

    for c in cities:
        r = get_weather_data(c.name)
        weather = {
            'city' : c.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    new_city = new_city.lower()
    new_city = string.capwords(new_city)
    if new_city:
        existing_city = city.query.filter_by(name=new_city).first()
        
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = city(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'That is not a valid city!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully!', 'success')

    return redirect(url_for('index_get'))

@app.route('/delete/<name>')
def delete_city( name ):
    c = city.query.filter_by(name=name).first()
    db.session.delete(c)
    db.session.commit()

    flash(f'Successfully deleted { c.name }!', 'success')
    return redirect(url_for('index_get'))