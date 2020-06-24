from flask import Blueprint, request, send_file
import requests

from app.api.utils import good_json_response, bad_json_response
from app.database import users, friends, uploads, posts
from app.database import skills, languages, hobbies
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.upload import get_file, save_file
from app.api import auth_username
from app.utils import ping, get_central_ip, get_own_ip, get_user_ip
from passlib.hash import sha256_crypt
from app.api import jwt_required_custom


from app.migrate import export

blueprint = Blueprint('data_user', __name__)


@blueprint.route('/', strict_slashes=False)
@jwt_required_custom
def user():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    user_details = users.export(
        'username', 'firstname', 'lastname', 'uploads_id',
        'location', 'study', 'bio', 'creation_date',
        'last_edit_date', 'relationship_status', 'phone_number',
        username=username
    )

    if not user_details:
        return bad_json_response("User not found")

    # Check what the status of the friendship is between the users
    friend_status = is_friend(username)
    if username == get_jwt_identity():
        friend_status = 1

    # Get image
    up_id = user_details[0][3]
    imageurl = "../static/images/default.jpg"
    if friend_status == 1 and uploads.exists(id=up_id):
        filename = uploads.export_one('filename', id=up_id)
        imageurl = get_own_ip() + 'file/{}/{}'.format(up_id, filename)

    # Basic information visible if not friends
    basic_info = {
        'username': user_details[0][0],
        'friend' : friend_status,
        'image_url': imageurl
    }

    if friend_status != 1:
        return good_json_response(basic_info)

    # All information visible if friends
    sensitive_info = {
        'firstname': user_details[0][1],
        'lastname': user_details[0][2],
        'location': user_details[0][4],
        'study': user_details[0][5],
        'bio': user_details[0][6],
        'creation_date': str(user_details[0][7]),
        'last_edit_date': str(user_details[0][8]),
        'relationship_status': user_details[0][9],
        'phone_number': user_details[0][10]

    }

    return good_json_response({**basic_info, **sensitive_info})


def is_friend(username):
    """
     Returns what the status of the friendship is between the
     logged in user and the given argument username
    # 0: no friendship
    # 1: friends
    # 2: friendship request is sent, waiting for response..
    # 2: friendship request received, sender is waiting for reply
    """
    if friends.exists(username=get_jwt_identity(), friend=username):
        friend_details = friends.export_one('accepted', 'sender', username=get_jwt_identity(), friend=username)
        if int(friend_details[0]) == 1:
            return 1 # accepted = 1
        if int(friend_details[1]) == 1:
            return 2 # pending
        return 3 # acceptable

    if friends.exists(username=username, friend=get_jwt_identity()):
        friend_details = friends.export_one('accepted', 'sender', username=username, friend=get_jwt_identity())
        if int(friend_details[0]) == 1:
            return 1 # accepted = 1
        if int(friend_details[1]) == 1:
            return 3 # acceptable
        return 2 # pending


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
@jwt_required_custom
def user_posts():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Check if user id exists
    if not users.exists(username=username):
        return bad_json_response('User not found.')

    # Send no data in case the users are not friends
    if username != get_jwt_identity() and is_friend(username) != 1:
        return good_json_response({'posts' : {} })

    return good_json_response({
        'posts': get_posts(username)
    })


def get_posts(username):
    # Get all posts of a user.
    user_posts = posts.export('id', 'title', 'body', 'creation_date', username=username)

    # Transfrom to array including dictionaries
    posts_array = [{
            'post_id' : item[0],
            'title' : item[1],
            'body' : item[2],
            'creation_date' : str(item[3]),
            'username'  : username
        }
        for item in user_posts
    ]

    return  posts_array


@blueprint.route('/timeline', methods=['GET'])
@jwt_required_custom
def timeline():
    from app.api.data.friend import get_friends

    username = get_jwt_identity()
    # Check if user exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # Get the user's own posts
    posts_array = get_posts(username)

    # Get the user's friends
    friends = get_friends(username)
    
    for i in range(0, len(friends)):
        try:
            friend = friends[i]['username']
            friend_address = get_user_ip(friend)
            # Get the posts of the friend
            response = requests.get(friend_address + '/api/user/posts?username='+friend, headers=request.headers).json()
            if response['success'] == True:
                posts = response['data']['posts']
                posts_array = posts_array + posts
        except:
            continue

    import datetime
    posts_array = sorted(posts_array, key=lambda k:
        datetime.datetime.strptime(k['creation_date'], "%Y-%m-%d %H:%M:%S"), reverse=True)

    return good_json_response({
        'posts': posts_array
    })


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    if not users.exists(username=username):
        return bad_json_response("User does not exist yet. Feel 'free' to join FedNet! :)")

    password_db = users.export('password', username=username)[0]

    if not sha256_crypt.verify(password, password_db):
        return bad_json_response("Password is incorrect.")

    email_confirmed = users.export_one("email_confirmed", username=username)
    if not email_confirmed:
        return bad_json_response("The email for this user is not authenticated yet. Please check your email.")

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

    if users.exists(email=request.form['email']):
        return bad_json_response('A user with this email is already registered on this data server.')

    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = sha256_crypt.encrypt(request.form['password'])

    users.insert(username=username, firstname=firstname,
                lastname=lastname, password=password, email=email)

    return good_json_response("success")


@blueprint.route('/deleteupload')
def deleteupload():
    uploads_id = request.args.get('uploads_id')

    if not uploads.exists(uploads_id=uploads_id):
        return bad_json_response('BIG OOPS: Something went wrong deleting the file.')

    uploads.delete(uploads_id=uploads_id)

    return good_json_response("success")


@blueprint.route('/delete', methods=['POST'])
@jwt_required_custom
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
@jwt_required_custom
def edit():
    username = get_jwt_identity()
    # username = request.form['username']

    if 'new_firstname' in request.form:
        new_firstname = request.form['new_firstname']
        users.update({'firstname':new_firstname}, username=username)

    if 'new_lastname' in request.form:
        new_lastname = request.form['new_lastname']
        users.update({'lastname':new_lastname}, username=username)

    if 'file' in request.files:
        image_filename = request.files['file'].filename
        image = request.files['file'].read()
        if image is not 0:
            uploads_id = save_file(image, filename=image_filename)

            if uploads_id is not False:
                users.update({'uploads_id' : uploads_id}, username=username)

    if 'new_location' in request.form:
        new_location = request.form['new_location']
        users.update({'location':new_location}, username=username)

    if 'new_study' in request.form:
        new_study = request.form['new_study']
        users.update({'study':new_study}, username=username)

    if 'new_bio' in request.form:
        new_bio = request.form['new_bio']
        users.update({'bio':new_bio}, username=username)

    if 'new_password' in request.form:
        new_password = sha256_crypt.encrypt(request.form['new_password'])
        users.update({'password':new_password}, username=username)

    if 'new_relationship_status' in request.form:
        new_relationship_status = request.form['new_relationship_status']
        users.update({'relationship_status':new_relationship_status}, username=username)

    if 'new_phone_number' in request.form:
        new_phone_number = request.form['new_phone_number']
        users.update({'phone_number':new_phone_number}, username=username)

    return good_json_response("success")

@blueprint.route('/password', methods=['POST'])
@jwt_required_custom
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


def forgotpassword():
    username = request.form['username']
    password = request.form['password']

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    newPassword = sha256_crypt.encrypt(request.form['password'])

    users.update({'password':newPassword}, username=username)

    return good_json_response("Succes")


@blueprint.route('/hobby')
@jwt_required_custom
def hobby():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    hobbies_details = hobbies.export('id', 'title', username=username)

    hobbies_array = [{
            'id' : item[0],
            'title' : item[1]
        }
        for item in hobbies_details
    ]

    return good_json_response({
        'hobbies': hobbies_array
    })


@blueprint.route('/addHobby', methods=['POST'])
@jwt_required_custom
def addHobby():
    username = get_jwt_identity()
    # username = request.form['username']

    title = request.form['title']

    hobbies.insert(username=username, title=title)

    return good_json_response("success")


@blueprint.route('/deleteHobby', methods=['POST'])
@jwt_required_custom
def deleteHobby():
    username = get_jwt_identity()

    id = request.form['id']

    hobbies.delete(id=id)

    return good_json_response("success")


@blueprint.route('/skill')
@jwt_required_custom
def skill():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    skill_details = skills.export(
            'id', 'title', 'skill_level' ,username=username
            )

    skill_array = [{
            'id' : item[0],
            'title' : item[1],
            'skill_level' : item[2]
        }
        for item in skill_details
    ]

    return good_json_response({
        'skills': skill_array
    })


@blueprint.route('/addSkill', methods=['POST'])
@jwt_required_custom
def addSkill():
    username = get_jwt_identity()

    title = request.form['title']
    skill_level = request.form['skill_level']

    skills.insert(username=username, title=title, skill_level=skill_level)

    return good_json_response("success")


@blueprint.route('/editSkill', methods=['POST'])
@jwt_required_custom
def editSkill():
    # username = get_jwt_identity()

    id = request.form['id']
    skill_level = request.form['skill_level']

    skills.update({'skill_level':skill_level}, id=id)

    return good_json_response('success')


@blueprint.route('/deleteSkill', methods=['POST'])
@jwt_required_custom
def deleteSkill():
    username = get_jwt_identity()

    id = request.form['id']

    skills.delete(id=id)

    return good_json_response("success")


@blueprint.route('/language')
@jwt_required_custom
def language():
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    language_details = languages.export(
            'id', 'title', 'skill_level' ,username=username
            )

    language_array = [{
            'id' : item[0],
            'title' : item[1],
            'skill_level' : item[2]
        }
        for item in language_details
    ]

    return good_json_response({
        'languages': language_array
    })


@blueprint.route('/addLanguage', methods=['POST'])
@jwt_required_custom
def addLanguage():
    username = get_jwt_identity()

    title = request.form['title']
    skill_level = request.form['skill_level']

    languages.insert(username=username, title=title, skill_level=skill_level)

    return good_json_response("success")


@blueprint.route('/deleteLanguage', methods=['POST'])
@jwt_required_custom
def deleteLanguage():
    username = get_jwt_identity()

    id = request.form['id']

    languages.delete(id=id)

    return good_json_response("success")


@blueprint.route('/editLanguage', methods=['POST'])
@jwt_required_custom
def editLanguage():
    username = get_jwt_identity()

    id = request.form['id']
    skill_level = request.form['skill_level']

    languages.update({'skill_level':skill_level}, id=id)

    return good_json_response('success')


@blueprint.route('/export')
@jwt_required_custom
def export_zip():
    username = get_jwt_identity()
    return send_file(export(username), mimetype='application/zip', as_attachment=True,
                     attachment_filename='export.zip')


@blueprint.route('/import', methods=['POST'])
@jwt_required_custom
def import_zip():
    username = get_jwt_identity()

    #get file
    if 'file' in request.files:
        file_filename = request.files['file'].filename
        file = request.files['file'].read()
        if file is not 0:
            # import file

            # file is the file to be imported
            # import(username, file)

            return good_json_response({'filename': file_filename})

__all__ = ('blueprint')
