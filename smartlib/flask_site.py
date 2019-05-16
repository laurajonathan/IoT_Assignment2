from flask import render_template, Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_forms import LoginForm
import requests, json

site = Blueprint("site", __name__)

# Webpage
@site.route('/')
@site.route('/index')
def index():
    # Use REST API
    response = requests.get("http://127.0.0.1:5000/book")
    books = json.loads(response.text)
    return render_template('smartlib.html', books = books)

@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('login.html')
