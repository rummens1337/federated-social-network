# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app
#from app import user

@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')




