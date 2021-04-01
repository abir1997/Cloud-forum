from flask import Blueprint, render_template, request, flash, jsonify
from main import app
import json

@app.route("/")
@app.route("/index")
def index():
    return render_template("home.html")
