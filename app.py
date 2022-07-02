#!/usr/bin/env python3
"""Module defines a flask app
"""
from time import sleep
from flask import Flask, flash, render_template, redirect, request, jsonify, url_for
from flask_socketio import SocketIO, emit, join_room
from uuid import uuid4
from copy import deepcopy
from models import storage
import bcrypt
from models.user import User

app = Flask(__name__, static_url_path='/static')
secret_key = str(uuid4())
app.config['SECRET_KEY'] = secret_key
sio = SocketIO(app)

# Game session dictionary
rooms = {}


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        jsonData = request.get_json()
        if rooms.get(jsonData['gameInterval']) is None:
            rooms[jsonData['gameInterval']] = str(uuid4())
            room = rooms[jsonData['gameInterval']]
        else:
            room = deepcopy(rooms[jsonData['gameInterval']])
            del rooms[jsonData['gameInterval']]
        return redirect(
            '/guest/{:s}'.format(room),
            code=302
            )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        password = request.form['password']
        age = request.form['age']
        email = request.form['email']
        usr = User()
        usr.first_name = first_name
        usr.last_name = last_name
        usr.user_name = user_name
        usr.password = bcrypt.hashpw(password.encode('utf-8'),
                                     bcrypt.gensalt())
        usr.email = email
        usr.age = age
        storage.new(usr)
        storage.save()
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        users = storage.all(User).values()
        hashed_password = None
        for user in users:
            if user.user_name == 'user_name':
                hashed_password = user.password
        if not hashed_password:
            message = "incorrect user name"
        print(hashed_password)
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            message="Incorrect password"
            flash('Incorrect password')
        else:
            message="Authentication success"
            redirect(url_for('index'))
    return render_template('signin.html')

@app.route('/guest/<room>')
def guest(room):
    return render_template('guest.html')


@sio.on('connect')
def on_connect():
    """Client connection listener"""
    emit('connected', {'data': 'Socket is online'})


@sio.on('join')
def on_join(data):
    join_room(data['room'])
    emit('room joined', 'joined room {:s}'.format(data['room']), to=data['room'])


@sio.on('communicate')
def on_communicate(data):
    emit('response', {'data': data['data'], 'sid': request.sid}, to=data['room'])


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000
    )
