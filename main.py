from flask import Flask, request, redirect, render_template, flash, session
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['Debug'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://put-the-db-login-path-here'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
app.secret_key='topsecretkey'

topics = []
points = [100, 200, 300, 400, 500]
correct_answer = 'test'


@app.route('/', methods=['GET'])
def index():
    session['score'] = 0
    return render_template('index.html')

@app.route('/jeopardy', methods=['GET','POST'])
def game():
    new_score = session['score']
    if request.method == 'POST':
        answer = request.form['answer']
        if (not answer):
            flash('Please enter something')
        else:
            if (answer == correct_answer):
                new_score += 1
                session['score'] = new_score
                return render_template('jeopardy.html', current_score = new_score)
            else:
                flash('Incorrect')
    return render_template('jeopardy.html', current_score = session['score'])
