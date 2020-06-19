from flask import Blueprint, request
import requests

from app.api.utils import good_json_response, bad_json_response
from app.database import users, friends, uploads, posts
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.upload import get_file, save_file
from app.api import auth_username
from app.utils import ping, get_central_ip, get_own_ip, get_user_ip
from passlib.hash import sha256_crypt
blueprint = Blueprint('data_user', __name__)


@blueprint.route('/', strict_slashes=False)
@jwt_required
def user():
    username = get_jwt_identity()

    if username is None:
        return bad_json_response('Authentication error: User not authenticated.')

    user_details = users.export(
        'username', 'firstname', 'lastname', 'uploads_id',
        'location', 'study', 'bio', 'creation_date',
        'last_edit_date',
        username=username
    )

    if not user_details:
        return bad_json_response("User not found")

    up_id = user_details[0][3]

    if up_id == None or up_id == 0:
        imageurl = "../static/images/default.jpg"
    else:
        data_ip = get_own_ip()
        response = requests.get(data_ip + '/api/file?id=' + str(up_id))
        url = response.json()['data']['url']
        imageurl = data_ip + url

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
        return bad_json_response('No users found.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/registered')
def registered():
    username = request.args.get('username')

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    if not users.exists(username = username):
        return bad_json_response('Username not found (in data server)')

    # for testing purposes; Enter your own IP address instead of ipaddress
    url = get_central_ip() + '/api/user/registered?username=' + username
    r = requests.get(url).json()

    return good_json_response(r)


@blueprint.route('/posts', methods=['GET'])
@jwt_required
def user_posts():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Check if user id exists
    if not users.exists(username=username):
        return bad_json_response('User not found.')

    # Get all posts of a user.
    user_posts = posts.export('title', 'body', 'creation_date', username=username)

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
        return bad_json_response("Bad request: Missing parameter 'username'.")

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    # TODO fail if user is already authenticated

    if not users.exists(username=username):
        return bad_json_response("User does not exist yet. Feel 'free' to join FedNet! :)")

    password_db = users.export('password', username=username)[0]

    if not sha256_crypt.verify(password, password_db):
        return bad_json_response("Password is incorrect.")

    # Login success
    access_token = create_access_token(identity=username)

    return good_json_response({
        'token' : access_token
    })


@blueprint.route('/register', methods=['POST'])
def register():
    """Registers a user to this data server."""
    # Exit early.
    if users.exists(username=request.form['username']):
        return bad_json_response('Username is already taken. Try again :)')

    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = sha256_crypt.encrypt(request.form['password'])

    users.insert(username=username, firstname=firstname,
                lastname=lastname, password=password, email=email)

    return good_json_response("success")

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
        return bad_json_response('BIG OOPS: Something went wrong deleting the file.')

    uploads.delete(uploads_id=uploads_id)

    return good_json_response("success")


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

        return good_json_response("success")
    else:
        return bad_json_response("Username is not registered.")


@blueprint.route('/edit', methods=['POST'])
@jwt_required
def edit():
    username = get_jwt_identity()
    # username = request.form['username']

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
        new_password = sha256_crypt.encrypt(request.form['new_password'])
        if 'new_password' != '':
            users.update({'password':new_password}, username=username)

    return good_json_response("success")

@blueprint.route('/password', methods=['POST'])
@jwt_required
def password():
    username = get_jwt_identity()
    password = request.form['oldPassword']

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    password_db = users.export('password', username=username)[0]

    if not sha256_crypt.verify(password, password_db):
        return bad_json_response("Password is incorrect.")

    if 'newPassword' in request.form:
        newPassword = sha256_crypt.encrypt(request.form['newPassword'])
    if 'newPassword' != '':
        users.update({'password':newPassword}, username=username)

    return good_json_response("Succes")

__all__ = ('blueprint')
