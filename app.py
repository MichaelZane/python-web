from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import os

app = Flask(__name__)



ENV = 'dev'

if ENV == 'dev':
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") 
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
   
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(30))
    phone = db.Column(db.Integer, (10))
    select_game = db.Column(db.String(200))
    time_played = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, email, name, phone, select_game, time_played, comments):
        self.email = email
        self.name = name
        self.phone = phone
        self.select_game = select_game
        self.time_played = time_played
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        select_game = request.form['select_game']
        time_played = request.form['time_played']
        comments = request.form['comments']
        

        if email == '' or select_game == '' or name == '':
            return render_template('index.html', message='Please enter required fields')

        if db.session.query(Feedback).filter(Feedback.email == email).count() == 0:
            data = Feedback(email, name, phone, select_game, time_played, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(email, name, phone, select_game, time_played, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')
        



if __name__ == '__main__':

    app.run()

     