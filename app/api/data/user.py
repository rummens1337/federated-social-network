import datetime

from flask import Blueprint, request, send_file
from flask_jwt_extended import create_access_token, get_jwt_identity
from passlib.hash import sha256_crypt
import requests

from app.api import auth_username, jwt_required_custom
from app.api.utils import good_json_response, bad_json_response
from app.database import users, friends, uploads, posts, skills, languages, \
    hobbies
from app.migrate import export_zip, import_zip
from app.upload import get_file, save_file
from app.utils import ping, get_central_ip, get_own_ip, get_user_ip

blueprint = Blueprint('data_user', __name__)


@blueprint.route('/', strict_slashes=False)
@jwt_required_custom
def user():
    """Get user details depending on friendship.

    If you are friends, sensitive data will be shown aswell.

    Returns:
        JSON reponse with the basic and sensitive user details.
    """
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Export used details of the user.
    user_details = users.export(
        'username', 'firstname', 'lastname', 'uploads_id',
        'location', 'study', 'bio', 'creation_date',
        'last_edit_date', 'relationship_status', 'phone_number',
        username=username
    )

    if not user_details:
        return bad_json_response('User not found')

    # Check what the status of the friendship is between the users.
    friend_status = is_friend(username)
    if username == get_jwt_identity():
        friend_status = 1

    # Get image.
    up_id = user_details[0][3]
    imageurl = '../static/images/default.jpg'
    if friend_status == 1 and uploads.exists(id=up_id):
        filename = uploads.export_one('filename', id=up_id)
        imageurl = get_own_ip() + 'file/{}/{}'.format(up_id, filename)

    # Basic information visible if not friends.
    basic_info = {
        'username': user_details[0][0],
        'friend': friend_status,
        'image_url': imageurl
    }

    if friend_status != 1:
        return good_json_response(basic_info)

    # All information visible if friends.
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


def get_profile_image(username):
    """Get the profile picture url.

    Args:
        username (string): The involved user.

    Returns:
        The image url.
    """
    up_id = users.export_one('uploads_id', username=username)

    # Get image url.
    imageurl = '../static/images/default.jpg'
    if uploads.exists(id=up_id):
        filename = uploads.export_one('filename', id=up_id)
        imageurl = get_user_ip(username) + '/file/{}/{}'.format(up_id, filename)

    return imageurl


def is_friend(username):
    """Return the status of the friendship.

    Looks up what the status of the frienship is between the logged in user and
    the given argument username.

    Args:
        username (string): The involved user.

    Returns:
        # 0: no friendship
        # 1: friends
        # 2: friendship request is sent, waiting for response..
        # 2: friendship request received, sender is waiting for reply
    """
    if friends.exists(username=get_jwt_identity(), friend=username):
        friend_details = friends.export_one('accepted', 'sender',
                                            username=get_jwt_identity(),
                                            friend=username)
        if int(friend_details[0]) == 1:
            return 1  # accepted = 1
        if int(friend_details[1]) == 1:
            return 2  # pending
        return 3  # acceptable

    if friends.exists(username=username, friend=get_jwt_identity()):
        friend_details = friends.export_one('accepted', 'sender',
                                            username=username,
                                            friend=get_jwt_identity())
        if int(friend_details[0]) == 1:
            return 1  # accepted = 1
        if int(friend_details[1]) == 1:
            return 3  # acceptable
        return 2  # pending


@blueprint.route('/all')
def users_all():
    """Get all usernames in the users table.

    Returns:
        JSON reponse that contains all the usernames in the users table.
    """
    usernames = users.export('username')

    if len(usernames) == 0:
        return bad_json_response('No users found.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/registered')
def registered():
    """Look up if the given username is a registered username in FedNet.

    Returns:
        JSON reponse that succeeds if the username is registered and
        fails if the user is not registered.
    """
    username = request.args.get('username')

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    if not users.exists(username=username):
        return bad_json_response('Username not found (in data server)')

    # This request checks if the given username is registered.
    r = requests.get(
        get_central_ip() + '/api/user/registered',
        params={
            'username': username
        }
    ).json()

    return good_json_response(r)


@blueprint.route('/posts', methods=['GET'])
@jwt_required_custom
def user_posts():
    """Retrieve all posts from a certain username.

    Checks are in place to check if the user is indeed a member of FedNet.
    This function uses the get_posts function below to actually retrieve the
    posts.

    Returns:
        JSON response that contains all posts of a certain user.
    """
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Check if user id exists.
    if not users.exists(username=username):
        return bad_json_response('User not found.')

    # Send no data in case the users are not friends.
    if username != get_jwt_identity() and is_friend(username) != 1:
        return good_json_response({'posts': {}})

    return good_json_response({
        'posts': get_posts(username)
    })


def get_posts(username):
    """Extract all the posts of a certain username from the
    posts table database.

    Args:
        username (string): The involved user.

    Returns:
        JSON response with all data from the posts table
    """
    # Get all posts of a user.
    user_posts = posts.export('id', 'title', 'body', 'creation_date',
                              'uploads_id', username=username)

    # Transfrom to array including dictionaries.
    posts_array = []

    for item in user_posts:
        up_id = item[4]
        imageurl = ''

        if uploads.exists(id=up_id):
            filename = uploads.export_one('filename', id=up_id)
            imageurl = get_own_ip() + 'file/{}/{}'.format(up_id, filename)

        posts_array.append({
            'post_id': item[0],
            'title': item[1],
            'body': item[2],
            'image_url': imageurl,
            'profile_image' : get_profile_image(username),
            'creation_date': str(item[3]),
            'username': username
        })
    return posts_array


@blueprint.route('/timeline', methods=['GET'])
@jwt_required_custom
def timeline():
    """This function handles the timeline, making sure you only see posts from
    the correct people.

    If you are friends with a certain user, that users posts will be shown in
    your timeline.

    Imported:
        get_friends function from api/data/friend.py

    Returns:
        JSON reponse that contains all the posts that are shown in the timeline.
    """
    from app.api.data.friend import get_friends

    username = get_jwt_identity()
    # Check if user exists.
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # Get the user's own posts.
    posts_array = get_posts(username)

    # Get the user's friends.
    friends = get_friends(username)

    for i in range(len(friends)):
        try:
            friend = friends[i]['username']
            friend_address = get_user_ip(friend)
            # Get the posts of the friend.
            response = requests.get(
                friend_address + '/api/user/posts',
                params={
                    'username': friend
                },
                headers=request.headers
            ).json()
            if response['success']:
                posts = response['data']['posts']
                posts_array = posts_array + posts
        except BaseException:
            continue

    posts_array = sorted(
        posts_array,
        key=lambda k: datetime.datetime.strptime(k['creation_date'],
                                                 '%Y-%m-%d %H:%M:%S'),
        reverse=True
    )

    return good_json_response({
        'posts': posts_array
    })


@blueprint.route('/login', methods=['POST'])
def login():
    """Function that handles the login.

    An access token is created. A check is in place to verify the encrypted
    password and to check if the user is verified through e-mail.

    Returns:
        A success JSON reponse that contains the access token.
    """
    username = request.form['username']
    password = request.form['password']

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    if not users.exists(username=username):
        return bad_json_response(
            "User does not exist yet. Feel 'free' to join FedNet! :)"
        )

    password_db = users.export('password', username=username)[0]

    # Verify the given password.
    if not sha256_crypt.verify(password, password_db):
        return bad_json_response('Password is incorrect.')

    # Check if the account has been verified through e-mail.
    email_confirmed = users.export_one('email_confirmed', username=username)
    if not email_confirmed:
        return bad_json_response(
            'The email for this user is not authenticated yet. '
            'Please check your email.'
        )

    # Login success.
    access_token = create_access_token(identity=username)

    return good_json_response({
        'token': access_token
    })


@blueprint.route('/register', methods=['POST'])
def register():
    """Registers a user to this data server.

    All the given information is stored in the users table in the database.
    """
    # Exit early.
    if users.exists(username=request.form['username']):
        return bad_json_response('Username is already taken. Try again :)')

    if users.exists(email=request.form['email']):
        return bad_json_response(
            'A user with this email is already registered on this data server.'
        )

    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = sha256_crypt.encrypt(request.form['password'])

    users.insert(username=username, firstname=firstname, lastname=lastname,
                 password=password, email=email)

    return good_json_response('success')


@blueprint.route('/deleteupload')
def deleteupload():
    """Deletes an upload.

    An uploads_id is given and that entry is then removed from the uploads table
    in the database.
    """
    uploads_id = request.args.get('uploads_id')

    if not uploads.exists(uploads_id=uploads_id):
        return bad_json_response(
            'BIG OOPS: Something went wrong deleting the file.'
        )

    uploads.delete(uploads_id=uploads_id)

    return good_json_response('success')


@blueprint.route('/delete', methods=['POST'])
@jwt_required_custom
def delete():
    """Delete a user from FedNet.

    The users details in the users table are deleted.
    """
    username = get_jwt_identity()

    if users.exists(username=username):
        # Everything that belongs to user is deleted automatically.
        users.delete(username=username)

        return good_json_response({'user': username})
    else:
        return bad_json_response('Username is not registered.')


@blueprint.route('/edit', methods=['POST'])
@jwt_required_custom
def edit():
    """Edit all your personal information and profile picture.

    All the correct tables are updated accordingly after an edit has been
    submitted.
    """
    username = get_jwt_identity()

    if 'new_firstname' in request.form:
        new_firstname = request.form['new_firstname']
        users.update({'firstname': new_firstname}, username=username)

    if 'new_lastname' in request.form:
        new_lastname = request.form['new_lastname']
        users.update({'lastname': new_lastname}, username=username)

    if 'file' in request.files:
        image_filename = request.files['file'].filename
        image = request.files['file'].read()
        if image is not 0:
            uploads_id = save_file(image, filename=image_filename)

            if uploads_id is not False:
                users.update({'uploads_id': uploads_id}, username=username)

    if 'new_location' in request.form:
        new_location = request.form['new_location']
        users.update({'location': new_location}, username=username)

    if 'new_study' in request.form:
        new_study = request.form['new_study']
        users.update({'study': new_study}, username=username)

    if 'new_bio' in request.form:
        new_bio = request.form['new_bio']
        users.update({'bio': new_bio}, username=username)

    if 'new_password' in request.form:
        new_password = sha256_crypt.encrypt(request.form['new_password'])
        users.update({'password': new_password}, username=username)

    if 'new_relationship_status' in request.form:
        new_relationship_status = request.form['new_relationship_status']
        users.update({'relationship_status': new_relationship_status},
                     username=username)

    if 'new_phone_number' in request.form:
        new_phone_number = request.form['new_phone_number']
        users.update({'phone_number': new_phone_number}, username=username)

    return good_json_response('success')


@blueprint.route('/password', methods=['POST'])
@jwt_required_custom
def password():
    """Upon entering the old password, a new password can be set.

    The old password is verified and the new password is encrypted and updated
    in the database.
    """
    username = get_jwt_identity()
    password = request.form['oldPassword']

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    password_db = users.export('password', username=username)[0]

    if not sha256_crypt.verify(password, password_db):
        return bad_json_response('Password is incorrect.')

    if 'newPassword' in request.form:
        new_password = sha256_crypt.encrypt(request.form['newPassword'])
    if 'newPassword' != '':
        users.update({'password': new_password}, username=username)

    return good_json_response('Succes')


def forgotpassword():
    username = request.form['username']
    password = request.form['password']

    if password is None:
        return bad_json_response("Bad request: Missing parameter 'password'.")

    new_password = sha256_crypt.encrypt(request.form['password'])

    users.update({'password': new_password}, username=username)

    return good_json_response('Succes')


@blueprint.route('/hobby')
@jwt_required_custom
def hobby():
    """Get all hobby details from a certain user.

    Returns:
        JSON reponse with the hobby details from the hobbies table.
    """
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Extract all the needed data from the hobbies table in the database.
    hobbies_details = hobbies.export('id', 'title', username=username)

    hobbies_array = [
        {
            'id': item[0],
            'title': item[1]
        }
        for item in hobbies_details
    ]

    return good_json_response({
        'hobbies': hobbies_array
    })


@blueprint.route('/addHobby', methods=['POST'])
@jwt_required_custom
def add_hobby():
    """Add a hobby to the hobbies table for a certain user. """
    username = get_jwt_identity()

    title = request.form['title']

    hobbies.insert(username=username, title=title)

    return good_json_response('success')


@blueprint.route('/deleteHobby', methods=['POST'])
@jwt_required_custom
def delete_hobby():
    """Delete a hobby entry from the hobbies table for a certain user. """
    username = get_jwt_identity()

    id = request.form['id']

    hobbies.delete(id=id)

    return good_json_response('success')


@blueprint.route('/skill')
@jwt_required_custom
def skill():
    """Get all skill details from a certain user.

    Returns:
        JSON reponse with the skill details from the skills table.
    """
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Extract all the needed data from the skills table in the database.
    skill_details = skills.export('id', 'title', 'skill_level',
                                  username=username)

    skill_array = [
        {
            'id': item[0],
            'title': item[1],
            'skill_level': item[2]
        }
        for item in skill_details
    ]

    return good_json_response({
        'skills': skill_array
    })


@blueprint.route('/addSkill', methods=['POST'])
@jwt_required_custom
def add_skill():
    """Add a skill to the skills table for a certain user. """
    username = get_jwt_identity()

    title = request.form['title']
    skill_level = request.form['skill_level']

    skills.insert(username=username, title=title, skill_level=skill_level)

    return good_json_response('success')


@blueprint.route('/editSkill', methods=['POST'])
@jwt_required_custom
def edit_skill():
    """Edit a skill entry in the skills table for a certain user. """
    id = request.form['id']
    skill_level = request.form['skill_level']

    skills.update({'skill_level': skill_level}, id=id)

    return good_json_response('success')


@blueprint.route('/deleteSkill', methods=['POST'])
@jwt_required_custom
def delete_skill():
    """Delete a skill entry from the skills table for a certain user. """
    username = get_jwt_identity()
    id = request.form['id']

    skills.delete(id=id)

    return good_json_response('success')


@blueprint.route('/language')
@jwt_required_custom
def language():
    """Get all language details from a certain user.

    Returns:
        JSON reponse with the language details from the languages table.
    """
    username = request.args.get('username')

    if username is None or username == '':
        username = auth_username()

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Extract all the needed data from the language table in the database.
    language_details = languages.export('id', 'title', 'skill_level',
                                        username=username)

    language_array = [
        {
            'id': item[0],
            'title': item[1],
            'skill_level': item[2]
        }
        for item in language_details
    ]

    return good_json_response({
        'languages': language_array
    })


@blueprint.route('/addLanguage', methods=['POST'])
@jwt_required_custom
def add_language():
    """Add a language to the languages table for a certain user. """
    username = get_jwt_identity()

    title = request.form['title']
    skill_level = request.form['skill_level']

    languages.insert(username=username, title=title, skill_level=skill_level)

    return good_json_response('success')


@blueprint.route('/deleteLanguage', methods=['POST'])
@jwt_required_custom
def delete_language():
    """Delete a language entry from the languages table for a certain user. """
    username = get_jwt_identity()

    id = request.form['id']

    languages.delete(id=id)

    return good_json_response('success')


@blueprint.route('/editLanguage', methods=['POST'])
@jwt_required_custom
def edit_language():
    """Edit a language entry in the languages table for a certain user. """
    username = get_jwt_identity()
    id = request.form['id']
    skill_level = request.form['skill_level']

    languages.update({'skill_level': skill_level}, id=id)

    return good_json_response('success')


@blueprint.route('/export')
@jwt_required_custom
def export_zip_():
    """Export all the data of a certain user as a zip.

    Returns:
        If the user exists, the user details will be exported.
    """

    username = get_jwt_identity()

    if users.exists(username=username):
        return send_file(export_zip(username), mimetype='application/zip',
                         as_attachment=True, attachment_filename='export.zip')
    else:
        return bad_json_response('User does not exist in database.')


@blueprint.route('/import', methods=['POST'])
@jwt_required_custom
def import_zip_():
    """Import all the data of a certain user.

    Returns:
        Success JSON response in case the import was successful.
        Else the bad JSON response will be returned with an error message.
    """
    username = get_jwt_identity()

    if 'file' in request.files:
        file = request.files['file'].read()
        if file is not 0:
            import_zip(file, username=username)
            return good_json_response()
    return bad_json_response('File not received.')


__all__ = ('blueprint',)
