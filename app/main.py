from flask import render_template, flash, redirect, session, url_for, request, g, Markup, Blueprint

from app.database import db_test

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('test1.html')


@blueprint.route('/about')
def about():
    return render_template('about.html')


@blueprint.route('/db')
def db_test():
    # Test
    try:
        test_db()
    except Exception as e:
	    return(str(e))
    return "db added"

__all__ = ('blueprint')

