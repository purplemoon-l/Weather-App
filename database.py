import sqlite3
from app import db
conn = sqlite3.connect('weather1.db')
db.create_all()

#conn.execute('CREATE TABLE weather (name TEXT, addr TEXT, city TEXT, pin TEXT)')

conn.close()

app.config['SQLALCHEMY_DATABASE_URI'] = 'C:\sqlite\weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
db = SQLAlchemy(app)

class City(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)