from flask import render_template, flash, redirect, session, url_for, request, g, Markup, Blueprint

from app.database import test_db

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return "DATA SERVER"


__all__ = ('blueprint')

