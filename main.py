from flask import Flask, request, redirect, render_template, flash, session
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['Debug'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://put-the-db-login-path-here'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
# app.secret_key = 'topsecretkey'

answer = "Jeopardy"
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet_remaining = ''

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/jeopardy', methods=['GET','POST'])
def game():
    if request.method == 'POST':
        guess_letter = request.form['guess_letter']
        guess_word = request.form['guess_word']
        if (not guess_letter) and (not guess_word):
            flash('Please either guess a word or a letter')

    return render_template('jeopardy.html')
