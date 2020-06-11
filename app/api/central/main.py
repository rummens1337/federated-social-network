from flask import render_template, flash, redirect, session, url_for, request, g, Markup, Blueprint

from app.database import test_db

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/home')
def index():
    return render_template('index.html')

@blueprint.route('/about')
@blueprint.route('/?')
@blueprint.route('/help')
def about():
    return render_template('about.html')

@blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@blueprint.route('/profile')
@blueprint.route('/me')
def profile():
    return render_template('profile.html')

@blueprint.route('/login')
def login():
    return render_template('login.html')

@blueprint.route('/friend_list')
def friend_list():
    friends = [
        {
            'name': {'username': ' Bas'},
            'photo': {'photo_url': "https://st3.depositphotos.com/6672868/13701/v/450/depositphotos_137014128-stock-illustration-user-profile-icon.jpg"},
            'profile': {'profile_url': "https://google.nl"}
        },
        {
            'name': {'username': 'Felix'},
            'photo': {'photo_url': "https://st3.depositphotos.com/6672868/13701/v/450/depositphotos_137014128-stock-illustration-user-profile-icon.jpg"},
            'profile': {'profile_url': "https://google.nl"}
        },
    ]
    return render_template('friends_list.html', friend_list = friends)

@blueprint.route('/settings')
def settings():
    return render_template('settings.html')

@blueprint.route('/settings/profile')
def settingsProfile():
    profile = {
        'name': {'firstname': 'Coen', 'lastname': 'Nusse','username': 'Coen'},
        'photo': {'photo_url': "https://st3.depositphotos.com/6672868/13701/v/450/depositphotos_137014128-stock-illustration-user-profile-icon.jpg"},
        'email': {'emailadress': "coennusse@live.nl"}
        }

    return render_template('settingsProfile.html', profile = profile)

@blueprint.route('/settings/privacy')
def privacy():
    return render_template('settingsPrivacy.html')

@blueprint.route('/settings/server')
def server():
    return render_template('settingsServer.html')

@blueprint.route('/password')
def password():
    return render_template('password.html')


__all__ = ('blueprint')


