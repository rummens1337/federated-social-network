from flask import render_template, flash, redirect, session, url_for, request, g, Markup, Blueprint
from flask_jwt_extended import jwt_required

from app.database import test_db

blueprint = Blueprint('main', __name__)

@blueprint.route('/test')
def test():
    return render_template('testform.html')

@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/home')
@jwt_required
def index():
    return render_template('index.html')

@blueprint.route('/about')
@blueprint.route('/?')
@blueprint.route('/help')
def about():
    return render_template('about.html')

@blueprint.route('/signup')
def signup():
    return render_template('login.html')

@blueprint.route('/profile')
@blueprint.route('/me')
@jwt_required
def profile():
    return render_template('profile.html')

@blueprint.route('/profile/<username>')
def profile_of(username):
    return render_template('profile.html', username=username)

@blueprint.route('/registerserver')
def register():
    return render_template('registerServer.html')

@blueprint.route('/login')
def login():
    return render_template('login.html')

@blueprint.route('/logout')
def logout():
    return render_template('logout.html')

@blueprint.route('/friends')
@jwt_required
def friends():
    return render_template('friends.html')

@blueprint.route('/settings')
@jwt_required
def settings():
    return render_template('settings.html')

@blueprint.route('/settings/profile')
@jwt_required
def settingsProfile():
    profile = {
        'name': {'firstname': 'Coen', 'lastname': 'Nusse','username': 'Coen'},
        'photo': {'photo_url': "https://st3.depositphotos.com/6672868/13701/v/450/depositphotos_137014128-stock-illustration-user-profile-icon.jpg"},
        'email': {'emailadress': "coennusse@live.nl"}
        }

    return render_template('settings/profile.html', profile = profile)

@blueprint.route('/settings/privacy')
@jwt_required
def privacy():
    return render_template('settings/privacy.html')

@blueprint.route('/settings/server')
@jwt_required
def server():
    return render_template('settings/server.html')

@blueprint.route('/settings/password')
@jwt_required
def password():
    return render_template('settings/password.html')


__all__ = ('blueprint')
