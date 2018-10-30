from flask import Flask, request, redirect, render_template, flash, session
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['Debug'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://put-the-db-login-path-here'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
# app.secret_key = 'topsecretkey'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
