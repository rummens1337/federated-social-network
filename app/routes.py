# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app
#from app import user

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('test3.html')

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

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/settings/profile')
def settingsProfile():
    return render_template('settingsProfile.html')

@app.route('/settings/privacy')
def privacy():
    return render_template('settingsPrivacy.html')

@app.route('/settings/server')
def server():
    return render_template('settingsServer.html')

@app.route('/settings/password')
def password():
    return render_template('password.html')
