"""
This file contains api routes corresponding to a data server
in the central server.
"""

from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import servers
from app.utils import ping

blueprint = Blueprint('central_server', __name__)


@blueprint.route('/')
def get_servers():
    """Get a list of all servers.

    Returns:
        JSON response containing a list with the name, address and id
        of a server.
    """
    result = servers.export('name', 'address', 'id')

    return good_json_response({
        'servers': result
    })


@blueprint.route('/pub_key')
def pub_key():
    """Get the public key of a user.
    
    Returns:
        JSON response containing the public key of a user.
    """
    username = request.args.get('username')

    if username is None:
        return bad_json_response('No username')

    return good_json_response(get_pub_key(username))


def get_pub_key(username):
    """Helper function to get the public key of a user.
    
    Returns:
        The public key of a user if available, else a bad JSON response.
    """
    server_id = users.export_one('server_id', username=username)
    if server_id is None:
        return bad_json_response('No server_id')

    pub = servers.export_one('pub_key', id=server_id)
    if pub is None:
        return bad_json_response('No pub')

    return pub


@blueprint.route('/register', methods=['POST'])
def register():
    """Register a data server to the central server.

    For this registration, the server name and address are requested in the
    form. A check is performed to see if the server is live. Then the server
    is inserted into the servers table if it does not already exists.
    
    Returns:
        JSON response containing the server id and the public key
        at success, else a bad JSON response containing the error message.
    """
    name = request.form['name']
    address = request.form['address']

    pub_key = ping(address)
    if pub_key:
        if not servers.exists(address=address):
            result = servers.insert(
                name=name, address=address, pub_key=pub_key)
            return good_json_response({
                'server_id': result,
                'pub_key': pub_key
            })
        else:
            name = servers.export_one('name', address=address)
            return bad_json_response(
                'The data server at "'
                + address
                + '" is already registered by the name "'
                + name
                + '".'
            )
    else:
        return bad_json_response(
            'The data server at "'
            + address +
            '" did not respond. Is the installation correct?'
        )


__all__ = ('blueprint',)
