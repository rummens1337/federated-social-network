from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity,verify_jwt_in_request_optional
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import servers
from app.api import auth_username

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/', methods=['GET'])
def user():
    usernames = users.export('username', 'server_id')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })
    # TODO error handling if query fails

@blueprint.route('/createtestusers', methods=['GET'])
def createtestusers():
    # This function is used for testing.
    # Insert users in central database with default address.
    usernames = ['nick', 'auke', 'testuser']
    server = 1
    for username in usernames:
        if not users.exists(username=username):
            users.insert(username=username, server_id=server)
    return good_json_response()
    # TODO error handling if query fails


@blueprint.route('/address', methods=['GET'])
def address():
    username = request.args.get('username')
    
    # If username is not given, use the logged in username
    if username is None or username == '':
        username = auth_username()
    
    if username is None or username == '':
        return bad_json_response('Username should be given as parameter.')

    if users.exists(username=username):
        server_id = users.export_one('server_id', username=username)

        if not servers.exists(  id=server_id):
            bad_json_response('Server does not exist in database.')

        address = servers.export_one('address', id=server_id)
        return good_json_response({
            'address': address
        })
    else:
        return bad_json_response('Username does not exist in database.')


@blueprint.route('/registered', methods=['GET'])
def registered():
    # TODO check if they are connected to a server?
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    exists = users.exists(username=username)

    return good_json_response({
        'registered': exists
    })
    # TODO error handling if query fails


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    server_id = request.form['server_id']

    if not servers.exists(address=server_id):
        return bad_json_response("Server not in database.")

    server_id = servers.export_one('id', address=server_id)

    if not users.exists(username=username):
        users.insert(username=username, server_id=server_id)
    else:
        return bad_json_response("Username already exists in database.")

    return good_json_response("success")
    # TODO error handling if query fails


@blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    # username = request.form['username']
    username = get_jwt_identity()

    if users.exists(username=username):
        users.delete(username=username)
        return good_json_response()
    else:
        return bad_json_response("Username does not exist in database.")
    # TODO error handling if query fails


@blueprint.route('/edit', methods=['POST'])
@jwt_required
def edit():
    # username = request.args.get('username')
    username = get_jwt_identity()

    if users.exists(username=username):
        if 'new_address' in request.form:
            new_address = request.form['new_address']
            if 'new_address' != '':
                users.update({'address':new_address}, username=username)
    else:
        return bad_json_response('Username does not exist in database.')

    return good_json_response()
    # TODO error handling if query fails

__all__ = ('blueprint')
