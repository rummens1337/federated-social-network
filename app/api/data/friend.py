from flask import Blueprint, request
import requests

from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import friends

blueprint = Blueprint('data_friend', __name__)

central_server = "http://localhost:5000/api/"

@blueprint.route('/add', methods=['POST'])
@jwt_required
def register():
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
    if friends.exists(users_id = str(user_id[0]), friend = friend_username):
        return bad_json_response('friendship already exists')

    # register friendship in database
    friends.insert(users_id=str(user_id[0]), friend=friend_username)

    # TODO register friendship in database for friend

    return good_json_response({
        'usernames': user_id
    })

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
