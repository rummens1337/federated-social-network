from flask import Blueprint, request
import requests

from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import posts

blueprint = Blueprint('data_user', __name__)

central_server = "http://localhost:5000/api/"

@blueprint.route('/')
def user():
    usernames = users.export('username')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })

@blueprint.route('/exists')
def exist():

    # TODO: check with central server if user_exists
    return good_json_response()

@blueprint.route('/posts')
def posts():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # check if user id exists
    user_id = users.export('rowid', username=username)
    if not user_id:
        return bad_json_response('user not found')

    # TODO fail if user is not registered

    # TODO get all posts of a user.
    user_posts = posts.export('title', 'body', 'rowid', users_id = str(user_id[0]))

    if len(user_posts) == 0:
        return bad_json_response('User has no posts.')

    return good_json_response({
        'posts': user_posts
    })


@blueprint.route('/details')
def details():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO fail if user is not registered

    user_details = users.export('name', 'uploads_id', 'location', 'study', username=username)

    if not user_details:
        return bad_json_response("User not found")

    # TODO: Get image url

    # return good_json_response(user_details[0][1])

    return good_json_response({
        'username': username,
        'name': user_details[0][0],
        'image_url': 'https://www.xolt.nl/wp-content/themes/fox/images/placeholder.jpg',
        'creation_date': 'date',
        'location': user_details[0][2],
        'study': user_details[0][3]
    })


    # return good_json_response({
    #     'username': username,
    #     'name': name,
    #     'image_url': image_url,
    #     'creation_date': creation_date,
    #     'location': location,
    #     'study': study
    # })


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    location = request.form['location']
    study = request.form['study']

    image_filename = request.files['file'].filename
    image = request.files['file'].read()

    # TODO fail if user is already registered

    # TODO register user and save image

    return good_json_response()


@blueprint.route('/delete', methods=['POST'])
def delete():
    username = request.form['username']

    # TODO fail if user is not registered

    # TODO delete user from database and remove static data

    return good_json_response()


@blueprint.route('/edit', methods=['POST'])
def edit():
    username = request.form['username']

    # TODO fail if user is not registered

    if 'name' in request.form:
        # TODO replace name in database
        pass
    if 'file' in request.files:
        image_filename = request.files['file'].filename
        image = request.files['file'].read()
        # TODO replace image
    if 'location' in request.form:
        # TODO replace location in database
        pass
    if 'study' in request.form:
        # TODO replace study in database
        pass

    return good_json_response()

__all__ = ('blueprint')
