from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import create_access_token, get_jwt_identity, \
    verify_jwt_in_request_optional

from app.api import auth_username, jwt_required_custom
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import servers
from app.utils import ping

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/')
def user():
    usernames = users.export('username', 'server_id')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })
    # TODO error handling if query fails


@blueprint.route('/createtestusers')
def createtestusers():
    # This function is used for testing.
    # Insert users in central database with default address.
    usernames = ['nick', 'auke', 'testuser']
    server = 1
    for username in usernames:
        if not users.exists(username=username):
            users.insert(username=username, server_id=server)
        else:
            return bad_json_response('Username already exists.')
    return good_json_response('success')
    # TODO error handling if query fails


@blueprint.route('/search')
def search():
    username = request.args.get('username')
    # TODO: add 'like' function
    userlist = users.export('username', username=username, like_prefix=True,
                            like_suffix=True)

    if userlist is None or userlist == '':
        return bad_json_response('No users found')

    return good_json_response({
        'users': userlist
    })


@blueprint.route('/address')
def address():
    username = request.args.get('username')

    # If username is not given, use the logged in username
    if username is None or username == '':
        username = auth_username()

    if username is None or username == '':
        return bad_json_response("Bad request: Missing parameter 'username'.")

    if users.exists(username=username):
        server_id = users.export_one('server_id', username=username)

        if not servers.exists(id=server_id):
            bad_json_response('Server is not registered.')

        name, address = servers.export_one('name', 'address', id=server_id)
        return good_json_response({
            'name': name,
            'address': address,
            'username': username
        })
    else:
        return bad_json_response('User is not found.')


@blueprint.route('/registered')
def registered():
    # TODO check if they are connected to a server?
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    exists = users.exists(username=username)

    return good_json_response({
        'registered': exists
    })


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    address = request.form['server_address']

    if not servers.exists(address=address):
        return bad_json_response('Server is not registered.')

    server_id = servers.export_one('id', address=address)

    # Check if server is live.
    if ping(address):
        if not users.exists(username=username):
            users.insert(username=username, server_id=server_id)
        else:
            return bad_json_response('Username is already taken. Try again :).')
    else:
        return bad_json_response(
            'This data server is not available. '
            'Please contact the server owner.'
        )

    return good_json_response('success')


@blueprint.route('/delete', methods=['POST'])
@jwt_required_custom
def delete():
    # username = request.form['username']
    username = get_jwt_identity()

    if users.exists(username=username):
        users.delete(username=username)
        return good_json_response()
    else:
        return bad_json_response('No user found with the username ' + username)


@blueprint.route('/edit', methods=['POST'])
@jwt_required_custom
def edit():
    # username = request.args.get('username')
    username = get_jwt_identity()

    if users.exists(username=username):
        if 'new_address' in request.form:
            new_address = request.form['new_address']
            #new_address = request.args.get('new_address')
            if 'new_address' != '':
                if servers.exists(address=new_address):
                    new_id = servers.export_one('id', address=new_address)
                    users.update({'server_id': new_id}, username=username)
                    return good_json_response({'new_address': new_address})
                else:
                    return bad_json_response(
                        'This address does not exist in the database.'
                    )
            else:
                return bad_json_response('Address undefined.')
        else:
            return bad_json_response('Incorrect form.')
    else:
        return bad_json_response(
            'No user found with the username ' + username + '.'
        )

__all__ = ('blueprint',)

