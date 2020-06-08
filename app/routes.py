# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app
#from app import user

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('test1.html')

@app.route('/about')
@app.route('/?')
@app.route('/help')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/profile')
@app.route('/me')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')
