from flask import Flask, Blueprint, render_template, request, flash, jsonify, url_for
from werkzeug.utils import redirect

import firebase_service as fbs
app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    users = fbs.get_all_users()
    print(request.form['userId'])
    if request.method == 'POST':
        if request.form['userId'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            print("Auth success")
            #return redirect(url_for('home'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)