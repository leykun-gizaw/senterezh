#!/usr/bin/env python3
"""Module defines a flask app
"""
from time import sleep
from flask import Flask, render_template, request, jsonify, redirect
from flask_socketio import SocketIO, emit, join_room
from uuid import uuid4
from copy import deepcopy

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
