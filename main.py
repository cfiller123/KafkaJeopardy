from flask import Flask, request, redirect, render_template, flash, session
import json
import random
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz, process

app = Flask(__name__)
app.config['Debug'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kafkaJeopardy:password@localhost:8889/kafkajeopardy'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='topsecretkey'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    score = db.Column(db.Integer)
    def __init__(self, name):
        self.name = name
        self.score = 0

@app.before_request
def require_user():
    allowed_routes = ['index']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def index():
    session['score'] = 0
    if request.method == 'POST':
        name = request.form['name']
        existing_user = User.query.filter_by(name = name).first()
        if (not name):
            flash('Please enter your name')
        elif(existing_user):
            flash('Welcome back!')
            session['user'] = name
            return redirect('/jeopardy')
        else:
            session['user'] = name
            new_user = User(name)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/jeopardy')
    return render_template('index.html')

@app.route('/jeopardy', methods=['GET','POST'])
def game():
    if request.method == 'POST':
        answer = request.form['answer']
        if (not answer):
            flash('Please enter something')
        else:
            if (fuzzy_match(answer,session['answer'],85)):
                current_user = User.query.filter_by(name = session['user']).first()
                current_user.score = current_user.score + 1
                db.session.commit()
                return render_template('jeopardy.html', current_score = current_user.score, question = question_selector())
            else:
                flash('Incorrect')
    current_user = User.query.filter_by(name = session['user']).first()
    return render_template('jeopardy.html', current_score = current_user.score, question = question_selector(), name = session['user'])

def question_selector():
    with open('JEOPARDY_QUESTIONS1.json') as file:
        data = json.load(file)
    x = random.randint(1,501)
    session['answer'] = data[x]['answer']
    return data[x]['question']

def fuzzy_match(guess, answer, acceptable_match):
    match = fuzz.ratio(guess,answer)
    if (match>=acceptable_match):
        return True
    else:
        return False

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')
    
if __name__ == '__main__':
    app.run()