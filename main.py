from flask import Flask, request, redirect, render_template, flash
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['Debug'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://put-the-db-login-path-here'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)

topics = []
points = [100, 200, 300, 400, 500]
score = 0


@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')

@app.route('/jeopardy', methods=['GET','POST'])
def game():
        if request.method == 'POST':
                answer = request.form['question']
                if (not answer):
                        flash('Please enter something')
                else:
                        if (answer == correct_answer):
                                score += 1
                                return redirect('jeopardy.html', current_score = score)
                        else:
                                flash('You already entered this letter')
        else:
                return render_template('jeopardy.html', current_score = 0)
