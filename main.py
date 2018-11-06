from flask import Flask, request, redirect, render_template, flash, session
import json
import random
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz, process
from kafka import TopicPartition, KafkaConsumer, OffsetAndMetadata

# Sets application configurations
app = Flask(__name__)
app.config['Debug'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kafkaJeopardy:password@localhost:8889/kafkajeopardy'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='topsecretkey'

# User object for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    score = db.Column(db.Integer)
    def __init__(self, name):
        self.name = name
        self.score = 0

# Requires login to play game 
@app.before_request
def require_user():
    allowed_routes = ['index']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/') 

# Landing page where you "login" by entering your name
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

# Main game page - updates score based on user's answers
@app.route('/jeopardy', methods=['GET','POST'])
def game():
    if request.method == 'POST':
        answer = request.form['answer']
        if (not answer):
            flash('Please enter something')
        else:
            if (fuzzy_match(answer,session['answer'],85)):
                current_user = User.query.filter_by(name = session['user']).first()
                jeopardy_info = get_kafka_question()
                value = jeopardy_info[1]
                current_user.score = current_user.score + int(value[1:])
                db.session.commit()
                question = jeopardy_info[0]
                return render_template('jeopardy.html', current_score = current_user.score, question = question[1:-1], name = session['user'])
            else:
                flash('Incorrect')
                current_user = User.query.filter_by(name = session['user']).first()
                current_user.score = current_user.score - 1
                db.session.commit()
    current_user = User.query.filter_by(name = session['user']).first()
    jeopardy_info = get_kafka_question()
    value = jeopardy_info[1]
    question = jeopardy_info[0]
    return render_template('jeopardy.html', current_score = current_user.score, question = question[1:-1], name = session['user'])

# Allows for 85% or better match of answer in case of misspelling/capitalization errors by user
def fuzzy_match(guess, answer, acceptable_match):
    match = fuzz.ratio(guess,answer)
    if (match>=acceptable_match):
        return True
    else:
        return False

# Gets most recent uncommitted question from queue by the user's name as group
def get_kafka_question():
    topic = 'Jeopardy'
    group_id = session['user']
    servers = ['localhost:9092']
    partition = 0
    consumer = KafkaConsumer(topic, group_id = group_id, bootstrap_servers=servers, auto_offset_reset='earliest', consumer_timeout_ms=1000, max_poll_records=1, enable_auto_commit=False)
    for msg in consumer:
        meta = consumer.partitions_for_topic(msg.topic)
        partition_temp = TopicPartition(msg.topic,msg.partition)
        offsets = OffsetAndMetadata(msg.offset+1, meta)
        options = {partition_temp: offsets}
        temp = parse_message(msg.value)        
        session['answer'] = temp['answer']
        question = temp['question']
        value = temp['value']
        consumer.commit(offsets=options)
        break
    consumer.close(autocommit=False)
    try:
        return question,value
    except:
        return 'No new questions :('

# Provides dictionary of kafka message contents
def parse_message(msg):
    item = json.loads(msg)
    return {'question':item['question'], 'answer':item['answer'], 'value':item['value']}

# Logs out so someone else can play with their own score
@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')
    
if __name__ == '__main__':
    app.run()
