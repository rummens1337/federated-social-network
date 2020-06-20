from flask import Blueprint, request
import requests

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users, posts, uploads, friends
from app.utils import ping, get_central_ip, get_own_ip, get_user_ip

blueprint = Blueprint('data_friend', __name__)


@blueprint.route('/all')
@jwt_required
def get_friends():
    """Returns all the friends of a user

    Note:

    Example:

    Args:

    Returns:

    """
    username = get_jwt_identity()
    # Check if user exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    friendships = friends.export('friend', username=username)

    # TODO: request all other avalible user data from the friends

    return good_json_response({
        'friends': friendships
    })


@blueprint.route('/insert_friendship', methods=['POST'])
def insert_friendship():
    """Inserts a friendship in the database.

    Note:
        Don't use directly with the frontend. Use /add instead.

    Example:
        Example calls are assuming that 'user1' is a user in the data server.
        It also assumes that the friendship doesn't already exists.

        Case where users exists and friendship doesn't already exists:
        >>> [server address]/api/friend/insert_friendship?username=user1&friend_username=user2
        {"success": true}

        Case where user does not exist:
        >>> [server address]/api/friend/insert_friendship?username=user2&friend_username=user3
        {"success": false, "reason": "user not found"}

    Args:
        username: Username of the user in the data server.
        friend_username: Username of the other user.

    Returns:
        A json response with either a succes of a failure and reason of failure.

    """
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # check if user id exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # check if friendship already exists
    if friends.exists(username=username, friend=friend_username):
        return bad_json_response('friendship already exists')
    # register friendship in database
    friends.insert(username=username, friend=friend_username, request_sent=1)

    return good_json_response()


@blueprint.route('/accept_friendship', methods=['POST'])
def accept_friendship():
    """Checks if a friendship request was actually sent and accepts the friendship.

    Note:
        Don't use directly with the frontend. Use /add instead.

    Example:

    Args:

    Returns:

    """
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # check if user id exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # check if friendship already exists
    if friends.exists(username=username, friend=friend_username):
        return bad_json_response('friendship already exists')

    # Check if request was sent:
    # Get address from central server
    friend_address = get_user_ip(friend_username)
    if not friend_address:
        return bad_json_response('user not found in central database')

    response = requests.get(friend_address + '/api/friend/confirm_request?username=' +
                            friend_username + '&friend_username=' + username).json()

    if str(response['success']) != 'True':
        return bad_json_response('request denied')
    if response['data'] != 'True':
        return bad_json_response('request denieded')

    friends.insert(username=username, friend=friend_username)
    return good_json_response()


@blueprint.route('/confirm_request')
def confirm_request():
    """Confirms that a friendship is requested.

    Note:
        Don't use directly with the frontend. Use /add instead.

    Example:
        [server_address]/api/friend/confirm_request?username=user1&friend_username=user2

    Args:
        username: Username of the user that that sent the request.
        friend_username: Username of the user that recieved the request.
    Returns:

    """
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    if username is None:
        return bad_json_response('username should be given as parameter.')

    if friend_username is None:
        return bad_json_response('username should be given as parameter.')

    if not users.exists(username=username):
        return bad_json_response('user not found')

    confirm = friends.export(
        'request_sent', request_sent=1, username=username, friend=friend_username)

    if confirm:
        return good_json_response('True')
    else:
        return good_json_response('False')


@blueprint.route('/add', methods=['POST'])
@jwt_required
def register():
    """Adds a friendship between two users.

    Note:

    Example:

    Args:

    Returns:

    """
    # username = request.form['username']
    # friend_username = request.form['friend_username']
    username = get_jwt_identity()
    # username = request.args.get('username')
    friend_username = request.args.get('friend_username')
    if not users.exists(username=username):
        return bad_json_response('user not found')

    friend_address = get_user_ip(friend_username)
    if not friend_address:
        return bad_json_response('user not found in central database')

    data_server = get_own_ip()
    if not data_server:
        return bad_json_response('user not found in central database')
    # register friendship in database
    response1 = requests.post(data_server + '/api/friend/insert_friendship?username=' +
                              username + '&friend_username=' + friend_username)
    if str(response1.json()['success']) != 'True':
        return bad_json_response(response1.json()['reason'])

    # register friend in other database
    response2 = requests.post(friend_address + '/api/friend/accept_friendship?username=' +
                              friend_username + '&friend_username=' + username).json()
    if str(response2['success']) != 'True':
        friends.delete(username=username, friend=friend_username)
        return bad_json_response(response2['reason'])

    friends.update({'request_sent': 0, 'request_accepted': 1},
                   username=username, friend=friend_username)

    return good_json_response()


@blueprint.route('/accept_request', methods=['POST'])
@jwt_required
def accept_request():
    """Accepts a friendship request.

    Note:

    Example:

    Args:

    Returns:

    """
    username = get_jwt_identity()
    friend_username = request.form['friend_username']

    # Check if friendship EXISTS
    if not friends.exists(username=username, friend=friend_username):
        return bad_json_response('friendship not found')

    # update friendship
    friends.update({'request_accepted': 1},
                   username=username, friend=friend_username)

    return good_json_response()


@blueprint.route('/reject_request', methods=['POST'])
@jwt_required
def reject_request():
    """Rejects a friendship request

    Note:

    Example:

    Args:

    Returns:

    """
    username = get_jwt_identity()
    friend_username = request.form['friend_username']

    # Check if friendship EXISTS
    if not friends.exists(username=username, friend=friend_username):
        return bad_json_response('friendship not found')

    # update friendship
    data_server = get_own_ip()
    if not data_server:
        return bad_json_response('user not found in central database')

    response = requests.post(data_server + '/api/friend/delete_friendship?username=' +
                             friend_username + '&friend_username=' + username).json()
    return good_json_response(str(response))
    if str(response['success']) != 'True':
        return bad_json_response(response['reason'])

    return good_json_response()


@blueprint.route('/get_friend_requests')
@jwt_required
def get_friend_requests():
    """Returns all the recieved friend request.

    Note:

    Example:

    Args:

    Returns:

    """
    username = get_jwt_identity()

    # Check if user exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    friendships = friends.export(
        'friend', username=username, request_accepted=0)

    # TODO: request all other avalible user data from the friends

    return good_json_response({
        'friends': friendships
    })


@blueprint.route('/delete_friendship', methods=['POST'])
def delete_friendship():
    """Deletes a friendship from the database

    Note:
        This function should not be used directly by the frontend.
        Use /delete instead

    Example:

    Args:

    Returns:

    """
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # check if user id exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # check if friendship already exists
    if not friends.exists(username=username, friend=friend_username):
        return bad_json_response('friendship does not exists')

    # register friendship in database
    friends.update({'request_delete': 1}, username=username,
                   friend=friend_username)

    return good_json_response()


@blueprint.route('/accept_deletion', methods=['POST'])
def accept_deletion():
    """Accepts a deletion request.

    Note:
        This function should not be used directly by the frontend.
        Use /delete instead

    Example:

    Args:

    Returns:

    """
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # check if user id exists
    if not users.exists(username=username):
        return bad_json_response('user not found')

    # check if friendship already exists
    if not friends.exists(username=username, friend=friend_username):
        return bad_json_response('friendship does not exists')

    # Get address from central server
    friend_address = get_user_ip(friend_username)
    if not friend_address:
        return bad_json_response('user not found in central database')

    response = requests.get(friend_address + '/api/friend/confirm_deletion?username=' +
                            friend_username + '&friend_username=' + username).json()

    if str(response['success']) != 'True':
        return bad_json_response('request denied')
    if response['data'] != 'True':
        return bad_json_response('request denieded')

    friends.delete(username=username, friend=friend_username)
    return good_json_response()


@blueprint.route('/confirm_deletion')
def confirm_deletion():
    """Confirm that a deletion request was sent.

    Note:
        This function should not be used directly by the frontend.
        Use /delete instead

    Example:

    Args:

    Returns:

    """
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    if username is None:
        return bad_json_response('username should be given as parameter.')

    if friend_username is None:
        return bad_json_response('username should be given as parameter.')

    if not users.exists(username=username):
        return bad_json_response('user not found')

    confirm = friends.export(
        'request_sent', request_delete=1, username=username, friend=friend_username)

    if confirm:
        return good_json_response('True')
    else:
        return good_json_response('False')


@blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    """Deletes a friendship between two users.

    Note:

    Example:

    Args:

    Returns:

    """
    # username = request.form['username']
    # friend_username = request.form['friend_username']
    username = get_jwt_identity()
    # username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    if not users.exists(username=username):
        return bad_json_response('user not found')

    friend_address = get_user_ip(friend_username)
    if not friend_address:
        return bad_json_response('user not found in central database')

    # register friendship in database
    data_server = get_own_ip()
    if not data_server:
        return bad_json_response('user not found in central database')

    response1 = requests.post(data_server + '/api/friend/delete_friendship?username=' +
                              username + '&friend_username=' + friend_username)
    if str(response1.json()['success']) != 'True':
        return bad_json_response(response1.json()['reason'])

    # register friend in other database
    response2 = requests.post(friend_address + '/api/friend/accept_deletion?username=' +
                              friend_username + '&friend_username=' + username).json()
    if str(response2['success']) != 'True':
        friends.delete(username=username, friend=friend_username)
        return bad_json_response(response2['reason'])

    friends.delete(
        username=username, friend=friend_username)

    return good_json_response()

__all__ = ('blueprint')
