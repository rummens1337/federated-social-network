from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import servers

blueprint = Blueprint('central_server', __name__)


@blueprint.route('/', methods=['GET'])
def server():
    return "server"


@blueprint.route('/test')
def test():
    return "test"

@blueprint.route('/registerserver', methods=['POST'])
def registerserver():
    name = request.form['name']
    address = request.form['address']
    if not servers.exists(address=address):
        servers.insert(name=name, address=address)

__all__ = ('blueprint')
