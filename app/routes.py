# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from flaskext.mysql import MySQL
from app import app


# TODO: needs to be moved from here.
#       Might be safer in the run.py
#       However, setting the config 
#       details there does not same to work.
# def sql():
#     # app.config['MYSQL_DATABASE_USER'] = 'user'
#     # app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
#     # app.config['MYSQL_DATABASE_DB'] = 'db'
#     # app.config['MYSQL_DATABASE_HOST'] = 'mysql'
#     return MySQL(app)

mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Test
@app.route('/db')
def db():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("INSERT INTO test VALUES (1)")
    con.commit()
    con.close()
    return "db added"

