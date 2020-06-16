from flask import Blueprint, request
import requests

from app.api.utils import good_json_response, bad_json_response
from app.database import users, friends, uploads, posts
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.upload import get_file, save_file


blueprint = Blueprint('data_user', __name__)

central_server = "http://localhost:5000/api/"


@blueprint.route('/', strict_slashes=False)
@jwt_required
def user():
    user_id = request.args.get('user_id')

    if user_id is None:
        return bad_json_response('user_id should be given as parameter.')

    # TODO fail if user is not authenticated

    user_details = users.export(
        'username', 'name', 'uploads_id',
        'location', 'study', 'creation_date',
        'last_edit_date',
        id=user_id
    )

    if not user_details:
        return bad_json_response("User not found")

    # TODO: Get image url

    return good_json_response({
        'username': user_details[0][0],
        'name': user_details[0][1],
        'image_url': 'https://www.xolt.nl/wp-content/themes/fox/images/placeholder.jpg',
        'location': user_details[0][3],
        'study': user_details[0][4],
        'creation_date': str(user_details[0][5]),
        'last_edit_date': str(user_details[0][6])
    })


@blueprint.route('/all')
def users_all():
    usernames = users.export('username')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/registered')
def registered():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    if not users.exists(username = username):
        return bad_json_response('Username not found (in data server)')

    # for testing purposes; Enter your own IP address instead of ipaddress
    url = 'http://ipaddress:5000/api/user/registered?username=' + username
    r = requests.get(url).json()

    return good_json_response(r)


@blueprint.route('/posts')
@jwt_required
def user_posts():
    user_id = request.args.get('user_id')

    if user_id is None:
        return bad_json_response('user_id should be given as parameter.')

    # check if user id exists
    if not users.exists(id=user_id):
        return bad_json_response('user not found')

    # TODO fail if user is not authenticated

    # TODO get all posts of a user.
    user_posts = posts.export('title', 'body', users_id=user_id)

    if len(user_posts) == 0:
        return bad_json_response('User has no posts.')

    return good_json_response({
        'posts': user_posts
    })


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username is None:
        return bad_json_response('username should be given as parameter.')

    if password is None:
        return bad_json_response('password should be given as parameter.')

    # TODO fail if user is already authenticated
    if not users.exists(username=username):
        return bad_json_response("Login failed")

    user = users.export('id', 'password', username=username)[0]

    # TODO Safe string compare
    if user[1] != password:
        return bad_json_response("Login failed2")

    # Login success
    access_token = create_access_token(identity=user[0])

    return good_json_response({
        'token' : access_token
    })


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    location = request.form['location']
    study = request.form['study']

    image_filename = request.files['file'].filename
    image = request.files['file'].read()

    if users.exists(username=username):
        return bad_json_response('Username is already registered')

    users.insert(username=username, location=location, study=study, password='fakepassword', name='testerrrr')

    uploads_id = save_file(image, filename=image_filename)
    users.update({'uploads_id' : uploads_id}, username=username)

    return good_json_response({
        'rowid' : rowid,
        'username' : username,
        'location' : location,
        'study' : study,
        'filename' : image_filename
    })


@blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    username = request.form['username']

    # TODO delete user from database and remove static data
    # remove static data? Think it is done.
    if users.exists(username=username):
        user_id = users.export('rowid', username=username)
        users.delete(rowid=user_id)
        uploads.delete(rowid=user_id)
        posts.delete(rowid=user_id)
        friends.delete(rowid=user_id)

        return good_json_response()
    else:
        return bad_json_response("Username is not registered.")


@blueprint.route('/edit', methods=['POST'])
@jwt_required
def edit():
    username = request.form['username']

    if users.exists(username=username):
        if 'new_name' in request.form:
            new_name = request.form['new_name']
            if 'name' != '':
                users.update({'name':new_name}, username=username)
        if 'file' in request.files:
            image_filename = request.files['file'].filename
            image = request.files['file'].read()
            # TODO replace image
        if 'new_location' in request.form:
            new_location = request.form['new_location']
            if 'new_location' != '':
                users.update({'location':new_location}, username=username)
        if 'new_study' in request.form:
            new_study = request.form['new_study']
            if 'new_study' != '':
                users.update({'study':new_study}, username=username)
    else:
        return bad_json_response('Username does not exist in database.')

    return good_json_response()


__all__ = ('blueprint')
