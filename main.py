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
            users = fbs.get_all_users()
            print(users)
            if is_valid_login(user_id, pwd):
                print("Authorization successful, routing to forum..")
            else:
                print("Authorization unsuccessful.")
                error = "Invalid credentials"

    return render_template('login.html', error=error)


def is_valid_login(user_id, password):
    users = fbs.get_all_users()
    for user in users:
        if user['id'] == user_id and user['password'] == password:
            return True
    return False


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)