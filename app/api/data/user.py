from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users

blueprint = Blueprint('data_user', __name__)


@blueprint.route('/')
def user():
    usernames = users.export('username')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/posts')
def posts():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO fail if user is not registered

    # TODO lookup all post ids from a certain user and get the post_IDs
    # dummy:
    post_id = users.export_one('id', username=username)

    # TODO return actual posts by post_ids
    # posts = ["test1", "test2"]

    if len(post_id) == 0:
        return bad_json_response('User has no posts.')

    return good_json_response({
        'posts': posts
    })


@blueprint.route('/details')
def details():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO fail if user is not registered

    # TODO retrieve profile details (dummy)
    # dummy:
    location='Amsterdam'
    image_url='www.google.com'
    creation_date='01-06-2021'
    study='biology'
    username='ME'
    name='creator name'

    return good_json_response({
        'username': username,
        'name': name,
        'image_url': image_url,
        'creation_date': creation_date,
        'location': location,
        'study': study
    })


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

