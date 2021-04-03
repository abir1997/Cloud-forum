from flask import Flask, render_template, request, flash, jsonify, url_for
import json
from werkzeug.utils import redirect

import firebase_service as fbs
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['userId'] and request.form['password']:
            user_id = request.form['userId']
            pwd = request.form['password']

            if is_valid_login(user_id, pwd):
                print("Authorization successful, routing to forum..")
            else:
                print("Authorization unsuccessful.")
                error = "ID or password is invalid"

    return render_template('login.html', message=error)


def is_valid_login(user_id, password):
    users = fbs.get_all_users()
    for user in users:
        if user['id'] == user_id and user['password'] == password:
            return True
    return False


@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user_id = request.form['userId']
        pwd = request.form['password']
        username = request.form['userName']
        users = fbs.get_all_users()
        if id_exists(users, user_id):
            error = "The ID already exists."
        elif username_exists(users, username):
            error = "The username already exists"
        else:
            print("Registration successful. Creating record in firestore.")
            fbs.create_user(user_id, username, pwd)
    return render_template('register.html', message=error)


def is_valid_registration(user_id, username):
    users = fbs.get_all_users()
    for user in users:
        if user['id'] == user_id or user['user_name'] == username:
            return False
    return True


def id_exists(users, user_id):
    for user in users:
        if user['id'] == user_id:
            return True
    return False


def username_exists(users, username):
    for user in users:
        if user['user_name'] == username:
            return False


@app.route("/logout")
def logout():
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)