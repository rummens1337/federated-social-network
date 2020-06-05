# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app
#from app import user

@app.route('/')
@app.route('/index')
@app.route('/login')
def index():
    from flaskext.mysql import MySQL

    # mysql = MySQL()
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    # app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    # app.config['MYSQL_DATABASE_DB'] = 'EmpData'
    # app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    # mysql.init_app(app)

    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
