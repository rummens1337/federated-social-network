from flask import Blueprint, request
import requests

from app.api.utils import good_json_response, bad_json_response
from app.database import users, friends, uploads, posts
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.upload import get_file, save_file
from app.api import auth_username


blueprint = Blueprint('data_user', __name__)


@blueprint.route('/', strict_slashes=False)
@jwt_required
def user():
    username = get_jwt_identity()

    if username is None:
        return bad_json_response('username should be given as parameter.')

    # TODO fail if user is not authenticated

    user_details = users.export(
        'username', 'firstname', 'lastname', 'uploads_id',
        'location', 'study', 'bio', 'creation_date',
        'last_edit_date',
        username=username
    )

    if not user_details:
        return bad_json_response("User not found")

    # TODO: Get image url
    # image_filename = request.files['file'].filename
    # image = request.files['file'].read()

    # uploads_id = save_file(image, filename=image_filename)
    # users.update({'uploads_id' : uploads_id}, username=username)
    ipaddress = 'http://192.168.0.102:9000'
    up_id = users.export('uploads_id', username=username)

    response = requests.get(ipaddress + '/api/file?id=6')
    url = response.json()['data']['url']
    imageurl = ipaddress + url

    return good_json_response({
        'username': user_details[0][0],
        'firstname': user_details[0][1],
        'lastname': user_details[0][2],
        'image_url': imageurl,
        'location': user_details[0][4],
        'study': user_details[0][5],
        'bio': user_details[0][6],
        'creation_date': str(user_details[0][7]),
        'last_edit_date': str(user_details[0][8])
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


@blueprint.route('/posts', methods=['GET'])
@jwt_required
def user_posts():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response('username should be given as parameter.')

    # Check if user id exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # Get all posts of a user.
    user_posts = posts.export('title', 'body', 'creation_date', username=username)

    if len(user_posts) == 0:
        return bad_json_response('User has no posts.')

    # Transfrom to array including dictionaries
    posts_array = [{
            'title' : item[0],
            'body' : item[1],
            'creation_date' : str(item[2])
        }
        for item in user_posts
    ]

    return good_json_response({
        'posts': posts_array
    })

# TODO implement
@blueprint.route('/timeline', methods=['GET'])
@jwt_required
def timeline():
    return user_posts()


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

    password_db = users.export('password', username=username)[0]

    # TODO Safe string compare
    if password_db != password:
        return bad_json_response("Login failed2")

    # Login success
    access_token = create_access_token(identity=username)

    return good_json_response({
        'token' : access_token
    })


@blueprint.route('/register', methods=['POST'])
def register():
    """Registers a user to this data server."""
    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']

    if users.exists(username=username):
        return bad_json_response('Username is already registered')

    users.insert(username=username, firstname=firstname,
                lastname=lastname, password=password, email=email)

    return good_json_response("registered")

    # Do not remove yet: was used for file uploads!
    # location = request.form['location']
    # study = request.form['study']
    # password = request.form['password']
    # name = request.form['name']

    # image_filename = request.files['file'].filename
    # image = request.files['file'].read()
    # uploads_id = save_file(image, filename=image_filename)
    # users.update({'uploads_id' : uploads_id}, username=username)

@blueprint.route('/deleteupload')
def deleteupload():
    uploads_id = request.args.get('uploads_id')

    if not uploads.exists(uploads_id=uploads_id):
        return bad_json_response('Upload id is not in database')

    uploads.delete(uploads_id=uploads_id)

    return good_json_response()


@blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    username = request.form['username']

    uploads_id = users.export('uploads_id', username=username)

    if users.exists(username=username):
        users.delete(username=username)
        # I dont think we want to delete this upload?
        # Upload might be shared by 2 users?
        uploads.delete(uploads_id=uploads_id)
        posts.delete(username=username)
        friends.delete(username=username)

        return good_json_response()
    else:
        return bad_json_response("Username is not registered.")


@blueprint.route('/edit', methods=['POST'])
#@jwt_required
def edit():
    # username = get_jwt_identity()
    username = request.form['username']

    if 'new_firstname' in request.form:
        new_firstname = request.form['new_firstname']
        if 'firstname' != '':
            users.update({'firstname':new_firstname}, username=username)
    if 'new_lastname' in request.form:
        new_lastname = request.form['new_lastname']
        if 'lastname' != '':
            users.update({'lastname':new_lastname}, username=username)
    if 'file' in request.files:
        image_filename = request.files['file'].filename
        image = request.files['file'].read()

        uploads_id = save_file(image, filename=image_filename)
        users.update({'uploads_id' : uploads_id}, username=username)
    if 'new_location' in request.form:
        new_location = request.form['new_location']
        if 'new_location' != '':
            users.update({'location':new_location}, username=username)
    if 'new_study' in request.form:
        new_study = request.form['new_study']
        if 'new_study' != '':
            users.update({'study':new_study}, username=username)
    if 'new_bio' in request.form:
        new_bio = request.form['new_bio']
        if 'new_bio' != '':
            users.update({'bio':new_bio}, username=username)
    if 'new_password' in request.form:
        new_password = request.form['new_password']
        if 'new_password' != '':
            users.update({'password':new_password}, username=username)

    return good_json_response()


__all__ = ('blueprint')
