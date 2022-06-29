#!/usr/bin/env python3
"""Module defines a flask app
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/guest')
def guest():
    return render_template('guest.html')


if __name__ == "__main__":
    app.run(
        host='localhost',
        port=5000
    )
