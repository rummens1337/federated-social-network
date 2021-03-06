"""
This file contains api routes corresponding to a friend relations
on a data server.
"""

from urllib.parse import urlparse

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity
import requests

from app.api import jwt_required_custom
from app.api.utils import good_json_response, bad_json_response
from app.database import users, posts, uploads, friends
from app.utils import ping, get_central_ip, get_own_ip, get_user_ip

blueprint = Blueprint('data_friend', __name__)


@blueprint.route('/all')
@jwt_required_custom
def all_friends():
    """Return all the friends of a user.

    Returns:
        All the friends of a user.
    """
    username = get_jwt_identity()

    if not users.exists(username=username):
        return bad_json_response('user not found')

    return good_json_response({
        'friends': get_friends(username)
    })


def get_friends(username):
    """Return all the friends of a user.

    Note:
        Make sure username is validated before.

    Returns:
        All the friends of a user.
    """

    friendships = friends.export('friend', username=username, accepted=1)
    friendships2 = friends.export('username', friend=username, accepted=1)

    friends_array = [
        {
            'username': item
        }
        for item in friendships + friendships2
    ]

    return friends_array


@blueprint.route('/requests')
@jwt_required_custom
def requests_open():
    """Return all the friend requests of a user.

    Including accepted and sender information.
    If sender == 0: means that the request can be
        accepted by the user.
    If sender == 1: means that the request is pending.

    Returns:
        All the friend requests pending of a user.
    """
    username = get_jwt_identity()

    if not users.exists(username=username):
        return bad_json_response('user not found')

    friendships = friends.export('friend', 'accepted', 'sender', 'id',
                                 username=username, accepted=0, sender=0)
    friendships2 = friends.export('username', 'accepted', 'sender', 'id',
                                  friend=username, accepted=0, sender=1)

    friends_array = [
        {
            'username': item[0],
            'sender': item[2],
            'id': item[3]
        }
        for item in friendships + friendships2
    ]

    return good_json_response({
        'friends': friends_array
    })


@blueprint.route('/request/insert', methods=['POST'])
@jwt_required_custom
def request_insert():
    """Insert receiving request from other data server.

    Note:
        Don't use directly with the frontend. Use /add in send functions
        instead.

    Returns:
        JSON reponse with status of the request.
    """
    username = request.form['username']
    friend = request.form['friend']

    if not users.exists(username=username):
        return bad_json_response('user not found')

    # Check if friendship already exists
    # Return a good json reponse, because the friend can be on
    # the same data server.
    if friends.exists(username=username, friend=friend) \
            or friends.exists(username=friend, friend=username):
        return good_json_response('friendship already exists')

    # Get the friend's data server address and check if friend exists
    friend_address = get_user_ip(friend)
    if not friend_address:
        return bad_json_response('user not found in central database')

    friends.insert(username=username, friend=friend, sender=0)
    return good_json_response('Friendrequest inserted')


@blueprint.route('/request/accept', methods=['POST'])
@jwt_required_custom
def request_accept():
    """Handles friend request on accept.

    Note:
        Don't use directly with the frontend. Use /add in send functions
        instead.

    Returns:
        JSON reponse with status of the request.
    """
    username = request.form['username']
    friend = request.form['friend']
    accept = request.form['accept']

    if friend != get_jwt_identity():
        return bad_json_response('Authentication error')

    if not friends.exists(username=username, friend=friend):
        return bad_json_response('friendship request does not exist')

    request_db = friends.export_one('accepted', 'sender', username=username,
                                    friend=friend)

    # Check if already accepted.
    if int(request_db[0]) == 1:
        return bad_json_response('Request already accepted')

    # Only accept if it was the sender.
    if int(request_db[1]) != 1:
        return bad_json_response('User sent the request him/herself')

    # Update friendship.
    if int(accept) == 1:
        friends.update({'accepted': 1}, username=username, friend=friend)
    else:
        friends.delete(username=username, friend=friend)

    return good_json_response('Friend request accepted or declined')


@blueprint.route('/request/delete', methods=['POST'])
@jwt_required_custom
def request_delete():
    """Handles friend request on delete.

    Returns:
        JSON reponse with status of the request.
    """
    username = request.form['username']
    friend = request.form['friend']

    if username == friend:
        return bad_json_response('Username equals friend')

    if username != get_jwt_identity() and friend != get_jwt_identity():
        return bad_json_response('Not allowed')

    friends.delete(username=username, friend=friend)
    friends.delete(username=friend, friend=username)

    return good_json_response('Friend request deleted')


@blueprint.route('/add', methods=['POST'])
@jwt_required_custom
def add():
    """Adds a friendship between two users.

    Sets the sender on 1 for the user that is sending the request. Accepted is
    set on 0.

    Returns:
        JSON reponse with status of the request.
    """
    username = get_jwt_identity()
    friend = request.form['friend']

    if username == friend:
        return bad_json_response('Friend equals user')

    if not users.exists(username=username):
        return bad_json_response('user not found')

    # Check if friendship already exists.
    if friends.exists(username=username, friend=friend) \
            or friends.exists(username=friend, friend=username):
        return bad_json_response('friendship already exists')

    # Get the friend's data server address and check if friend exists.
    friend_address = get_user_ip(friend)
    if not friend_address:
        return bad_json_response('user not found in central database')

    # Add the friend in current dataserver's database.
    if not friends.insert(username=username, friend=friend, sender=1):
        return bad_json_response('error adding friend1')

    # Register friend in other database.
    data = {
        'username': friend,
        'friend': username
    }

    try:
        response = requests.post(
            friend_address + '/api/friend/request/insert',
            data=data,
            headers=request.headers
        ).json()
        if response['success']:
            return good_json_response('Friend request sent')

    except BaseException:
        friends.delete(username=username, friend=friend)
        return bad_json_response('Error while inserting')

    return bad_json_response('friend error')


@blueprint.route('/accept', methods=['POST'])
@jwt_required_custom
def accept():
    """Handles friend request on accept.

    Note:
        Don't use directly with the frontend. Use /add in send functions
        instead.

    Returns:
        JSON reponse with status of the request.
    """
    username = get_jwt_identity()
    request_id = request.form['id']
    accept = request.form['accept']

    # Check if friendship exists.
    if not friends.exists(id=request_id):
        return bad_json_response('friendship not found')

    # Send other user that it is accepted.
    # Can only accept if logged in user is the friend (request reciever).
    request_db = friends.export_one('username', 'friend', 'accepted', 'sender',
                                    id=request_id)
    friend = request_db[1]

    # Check if already accepted.
    if int(request_db[2]) == 1:
        return bad_json_response('Request already accepted')

    # Get the friend's data server address and check if friend exists.
    friend_address = get_user_ip(friend)
    if not friend_address:
        return bad_json_response('user not found in central database')

    if urlparse(get_own_ip()).netloc == urlparse(friend_address).netloc:
        if username != friend or request_db[3] != 1:
            return bad_json_response('Friend undefined error')
    else:
        # Check if not the sender and if the username is allowed to
        # accept the current request. If so, send the request to
        # the other data server.
        if request_db[3] == 1 or request_db[0] != username:
            return bad_json_response(
                'User sent the request him/herself or not authenticated'
            )

        data = {
            'username': friend,
            'friend': username,
            'accept': accept
        }
        try:
            response = requests.post(
                friend_address + '/api/friend/request/accept',
                data=data,
                headers=request.headers
            ).json()
            if not response['success']:
                return bad_json_response(response['reason'])
        except BaseException:
            return bad_json_response('Friend error2')

    # Update friendship in the data server's own database.
    if int(accept) == 1:
        friends.update({'accepted': 1}, id=request_id)
    else:
        friends.delete(id=request_id)

    return good_json_response('Friend request accepted or declined')


@blueprint.route('/delete', methods=['POST'])
@jwt_required_custom
def delete():
    """Handles friend request on delete.

    Returns:
        JSON reponse with status of the request.
    """
    username = get_jwt_identity()
    friend = request.form['friend']

    # Check if friendship exists.
    if not friends.exists(username=username, friend=friend) \
            and not friends.exists(username=friend, friend=username):
        return bad_json_response('friendship does not exist')

    # Get the friend's data server address and check if friend exists.
    friend_address = get_user_ip(friend)
    if not friend_address:
        return bad_json_response('user not found in central database')

    # Delete friendship in other data server.
    if urlparse(get_own_ip()).netloc != urlparse(friend_address).netloc:

        data = {
            'username': friend,
            'friend': username
        }
        try:
            response = requests.post(
                friend_address + '/api/friend/request/delete',
                data=data,
                headers=request.headers
            ).json()
            if not response['success']:
                return bad_json_response('Error while deleting1')
        except BaseException:
            return bad_json_response('Error while deleting2')

    # Delete in this database.
    friends.delete(username=username, friend=friend)
    friends.delete(username=friend, friend=username)

    return good_json_response('Friend deleted')
