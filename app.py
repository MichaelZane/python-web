from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/emailDB'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kwidfkqixdrrjo:8da91ee8628917104ba408d6d3f4c229e4e5aef42d6665f382ffc2f412af6b04@ec2-54-147-126-202.compute-1.amazonaws.com:5432/d1ggsdg6qv7lha'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    time_played = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, email, dealer, time_played, comments):
        self.email = email
        self.dealer = dealer
        self.time_played = time_played
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        select_game = request.form['select_game']
        time_played = request.form['time_played']
        comments = request.form['comments']
        

        if email == '' or select_game == '':
            return render_template('index.html', message='Please enter required fields')

        if db.session.query(Feedback).filter(Feedback.email == email).count() == 0:
            data = Feedback(email, select_game, time_played, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(email, select_game, time_played, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')
        



if __name__ == '__main__':

    app.run()

     