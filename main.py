from flask import Flask, Blueprint, render_template, request, flash, jsonify
import firebase_service as fbs
app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)