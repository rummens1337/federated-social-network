from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import create_access_token,get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import servers
from app.utils import ping

blueprint = Blueprint('central_server', __name__)


@blueprint.route('/', methods=['GET'])
def get_servers():
    """Returns a list of all servers."""
    result = servers.export('name', 'address', 'id')

    # Returns empty array if no servers found.
    return good_json_response({
        'servers': result
    })


@blueprint.route('/pub_key', methods=['GET'])
def pub_key():
    username = request.args.get('username')

    if username is None:
        return bad_json_response("No username")

    server_id = users.export_one('server_id', username = username)
    if server_id is None:
        return bad_json_response("No server_id")

    pub = servers.export_one('pub_key', id=server_id)
    if pub is None:
        return bad_json_response("No pub")

    return good_json_response(pub)

@blueprint.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    address = request.form['address']

    pub_key = ping(address)
    if pub_key:
        if not servers.exists(address=address):
            result = servers.insert(name=name, address=address, pub_key=pub_key)
            return good_json_response({
                'server_id': result,
                'pub_key':pub_key
            })
        else:
            name = servers.export_one('name', address=address)
            return bad_json_response('The data server at "' + address + '" is already registered by the name "' + name + '".')
    else:
        return bad_json_response('The data server at "' + address + '" did not respond. Is the installation correct?')

__all__ = ('blueprint')
