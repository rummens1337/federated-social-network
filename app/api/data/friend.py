from flask import Blueprint, request
import requests

from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import friends

blueprint = Blueprint('data_friend', __name__)

central_server = "http://localhost:5000/api"
data_server = "http://localhost:9000/api"


@blueprint.route('/check')
def check():
    username = request.args.get('username')
    #TODO: send request to central server to get address of the data server

    url = 'http://localhost:9000/api/friend/get_friends?username=' + username
    r = requests.get(url).json()
    #TODO: send request to data server to check if user exists

    return good_json_response(r)

@blueprint.route('/insert_friendship', methods=['POST'])
def insert_friendship():
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # check if user id exists
    user_id = users.export('rowid', username=username)
    if not user_id:
        return bad_json_response('user not found')

    #check if friendship already exists
    if friends.exists(users_id = str(user_id[0]), friend = friend_username):
        return bad_json_response('friendship already exists')

    # register friendship in database
    friends.insert(users_id=str(user_id[0]), friend=friend_username)

    return good_json_response({
        'usernames': user_id
    })

@blueprint.route('/add', methods=['POST'])
@jwt_required
def register():
    # username = request.form['username']
    # friend_username = request.form['friend_username']
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # TODO: get address of friend and fail if address is not avalible
    #dummy:
    friend_address = 'http://localhost:9000/api'

    # check if friend is registered on the address
    response = requests.get(friend_address + '/user/registered?username=' + friend_username)

    jr = response.json()['data']['registered']

    if jr != 'true':
        return bad_json_response('friend not found')


    # register friendship in database
    response1 = requests.post(friend_address + '/friend/insert_friendship?username=' + friend_username + '&friend_username=' + username)
    if not response1.json()['success']:
        return bad_json_response('could not reach friend')
    response2 = requests.post(data_server + '/friend/insert_friendship?username=' + username + '&friend_username=' + friend_username)

    return good_json_response()

@blueprint.route('/get_friends')
@jwt_required
def get_friends():
    username = request.args.get('username')

    # Check if user exists
    user_id = users.export('rowid', username=username)
    if not user_id:
        return bad_json_response('user not found')

    friendships = friends.export('friend', users_id = str(user_id[0]))

    # TODO: request all other avalible user data from the friends


    return good_json_response({
        'friends': friendships
    })

@blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    # username = request.form['username']
    # friend_username = request.form['friend_username']
    username = request.args.get('username')
    friend_username = request.args.get('friend_username')

    # TODO: check if friend exists

    # check if user id exists
    user_id = users.export('rowid', username=username)
    if not user_id:
        return bad_json_response('user not found')

    #check if friendship already exists
    friendship = friends.export('rowid', users_id = str(user_id[0]), friend = friend_username)
    if not friendship:
        return bad_json_response('friendship does not exists')

    # register friendship in database
    friends.delete(rowid = str(friendship[0]))

    # TODO: delete friendship for friend

    return good_json_response({
        'usernames': user_id
    })

__all__ = ('blueprint')
