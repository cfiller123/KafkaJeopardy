from flask import Flask, request, redirect, render_template, flash, session
import json
import random
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['Debug'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://put-the-db-login-path-here'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
app.secret_key='topsecretkey'

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
        if (not name):
            flash('Please enter your name')
        else:
            session['user'] = name
            return redirect('/jeopardy')
    return render_template('index.html')

@app.route('/jeopardy', methods=['GET','POST'])
def game():
    new_score = session['score']
    if request.method == 'POST':
        answer = request.form['answer']
        if (not answer):
            flash('Please enter something')
        else:
            if (answer == session['answer']):
                new_score += 1
                session['score'] = new_score
                return render_template('jeopardy.html', current_score = session['score'], question = question_selector())
            else:
                flash('Incorrect')
    return render_template('jeopardy.html', current_score = session['score'], question = question_selector(), name = session['user'])

def question_selector():
    with open('JEOPARDY_QUESTIONS1.json') as file:
        data = json.load(file)
    x = random.randint(1,501)
    session['answer'] = data[x]['answer']
    return data[x]['question']

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')
    
if __name__ == '__main__':
    app.run()