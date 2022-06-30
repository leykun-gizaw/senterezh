#!/usr/bin/env python3
"""Module defines a flask app
"""
from time import sleep
from flask import Flask, render_template, request, jsonify, redirect
from os import environ

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('index.html')
    jsonData = request.get_json()
    print(jsonData)
    if request.method == "POST":
        sleep(10)
        return redirect('/guest', code=302)


@app.route('/guest')
def guest():
    return render_template('guest.html')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(environ.get('PORT') or 5000)
    )
