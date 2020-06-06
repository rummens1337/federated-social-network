# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from flaskext.mysql import MySQL
from app import app

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
    try: 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("INSERT INTO test VALUES (1)")
        con.commit()
        con.close()
    except Exception as e:
	    return(str(e))
    return "db added"

