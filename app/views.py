from app import app, db
from flask import  (abort, flash,  redirect, render_template,
                   request, Response, session, url_for )
from app.models import User
from flask.ext.bcrypt import generate_password_hash, check_password_hash


import functools


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publications/')
def publications():
    return render_template('publications.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.errorhandler(404)
def not_found(exc):
    return Response('<h3>Not found</h3>'), 404
