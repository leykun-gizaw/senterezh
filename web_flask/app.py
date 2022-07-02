#!/usr/bin/python3


from flask import Flask, flash, redirect, render_template, request, url_for
from models import storage
from models.user import User
import bcrypt


app = Flask(__name__)


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


@app.route('/signin', methods=['GET', ['POST']])
def signin():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        hashed_password = ""    # to be queried from database
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            flash('Incorrect password')
        else:
            redirect(url_for('index'))
    return render_template('signin.html')
