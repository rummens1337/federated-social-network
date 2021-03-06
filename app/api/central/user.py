"""
This file contains api routes corresponding to a user in the central server.
"""

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
    """Get all usernames and their respective server ID's from the users table.

    Returns:
        JSON response containing all the usernames in the users table.
    """
    usernames = users.export('username', 'server_id')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/search')
def search():
    """Get usernames similar to the current letters typed into the search bar.

    For this function, like_prefix and like_suffix were added to the arguments
    of the export function.

    Returns:
        JSON response containing all the similar usernames.
        If there are no usernames similar to the one you tried to search for,
        a failed JSON response is returned.
    """
    username = request.args.get('username')

    userlist = users.export('username', username=username, like_prefix=True,
                            like_suffix=True)

    if userlist is None or userlist == '':
        return bad_json_response('No users found')

    return good_json_response({
        'users': userlist
    })


@blueprint.route('/address')
def address():
    """Get the address of a certain user.

    From the users and servers tables, necessary details are extracted from
    entries containing the given username.

    Returns:
        JSON response containing the address details of a certain user.
        If the user is not found or the server is non existant, a failed JSON
        response is returned.
    """
    username = request.args.get('username')

    # If username is not given, use the logged in username.
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
    """Check if a certain user is registered in the users table.

    Returns:
        JSON response containing username of the certain user if the user is
        indeed registered.
        If the username is not found, a failed JSON response is returned.
    """
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    exists = users.exists(username=username)

    return good_json_response({
        'registered': exists
    })


@blueprint.route('/register', methods=['POST'])
def register():
    """Register a user to the central server.

    For this registration, the username and server address are requested in the
    form. A check is performed to see if the server is live. Then the user is
    inserted into the users table.

    Returns:
        Success JSON response if the operation is successful.
        If the username is valid or the server is not live, a failed JSON
        response is returned.
    """
    username = request.form['username']
    address = request.form['server_address']

    if not servers.exists(address=address):
        return bad_json_response('Server is not registered.')

    server_id = servers.export_one('id', address=address)

    if ping(address):
        if not users.exists(username=username):
            users.insert(username=username, server_id=server_id)
        else:
            return bad_json_response(
                'Username is already taken. Try again :).')
    else:
        return bad_json_response(
            'This data server is not available. '
            'Please contact the server owner.'
        )

    return good_json_response('success')


@blueprint.route('/delete', methods=['POST'])
@jwt_required_custom
def delete():
    """Delete a certain user from the central server.

    The entry with the certain users username is removed from the users table in
    the database.

    Returns:
        Success JSON response if the operation is successful.
        Else a failed JSON response is returned with the correct error message.
    """
    username = get_jwt_identity()

    if users.exists(username=username):
        users.delete(username=username)
        return good_json_response()
    else:
        return bad_json_response('No user found with the username ' + username)


@blueprint.route('/edit', methods=['POST'])
@jwt_required_custom
def edit():
    """Edit a certain users details in the central server.

    The entry with the certain users username is edited in the users table in
    the database.

    Returns:
        Success JSON response if the operation is successful.
        Else a failed JSON response is returned with the correct error message.
    """
    username = get_jwt_identity()

    if users.exists(username=username):
        if 'new_address' in request.form:
            new_address = request.form['new_address']
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
