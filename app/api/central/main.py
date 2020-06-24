from flask import render_template, flash, redirect, session, url_for, request, g, Markup, Blueprint
from app.api import jwt_required_custom

from app.database import test_db

blueprint = Blueprint('main', __name__)

@blueprint.route('/test')
def test():
    return render_template('testform.html')

@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/home')
@jwt_required_custom
def index():
    return render_template('index.html')

@blueprint.route('/about')
@blueprint.route('/?')
@blueprint.route('/help')
def about():
    return render_template('about.html')

@blueprint.route('/about/serverSetup')
def serverSetup():
    return render_template('/about/serverSetup.html')

@blueprint.route('/about/joinServer')
def joinServer():
    return render_template('/about/joinServer.html')

@blueprint.route('/signup')
def signup():
    return render_template('login.html')

@blueprint.route('/profile')
@blueprint.route('/me')
@jwt_required_custom
def profile():
    return render_template('profile.html')

@blueprint.route('/profile/<username>')
@jwt_required_custom
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
@jwt_required_custom
def friends():
    return render_template('friends.html')

@blueprint.route('/friend/requests')
@jwt_required_custom
def friend_requests():
    return render_template('friend/requests.html')

@blueprint.route('/settings')
@jwt_required_custom
def settings():
    return render_template('settings.html')

@blueprint.route('/settings/profile')
@jwt_required_custom
def settingsProfile():
    return render_template('settings/profile.html', profile = profile)

@blueprint.route('/settings/privacy')
@jwt_required_custom
def privacy():
    return render_template('settings/privacy.html')

@blueprint.route('/settings/server')
@jwt_required_custom
def server():
    return render_template('settings/server.html')

@blueprint.route('/settings/password')
@jwt_required_custom
def password():
    return render_template('settings/password.html')

@blueprint.route('/settings/about')
@jwt_required_custom
def personalInfo():
    return render_template('settings/about.html')

@blueprint.route('/forgotPassword')
def changePassword():
    return render_template('changePassword.html')

@blueprint.route('/search')
@jwt_required_custom
def search_result():
    return render_template('search.html')


__all__ = ('blueprint')
