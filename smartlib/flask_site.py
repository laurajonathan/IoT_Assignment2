from flask import render_template, Flask, Blueprint, request, jsonify, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_forms import LoginForm
import requests, json

site = Blueprint("site", __name__)

# Webpage
@site.route('/')
@site.route('/index')
def index():
    if 'loggedin' in session:
        # Use REST API
        response = requests.get("http://127.0.0.1:5000/book")
        books = json.loads(response.text)
        return render_template('smartlib.html', books = books)
    else:
    	return redirect(url_for('site.login'))

@site.route('/data_visualization')
def data_visualization():
    if 'loggedin' in session:
        return render_template('data_visualization.html')
    else:
    	return redirect(url_for('site.login'))

@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "jaqen" and form.password.data == "hghar":
            session['loggedin'] = True
            return redirect('/index')
    return render_template('login.html', form = form)

@site.route('/logout', methods=['GET', 'POST'])
def logout():
	session.clear()
	return redirect('/login')