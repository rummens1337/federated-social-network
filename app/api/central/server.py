from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import servers

blueprint = Blueprint('cenral_server', __name__)


@blueprint.route('/', methods=['GET'])
def server():
    return "server"


@blueprint.route('/test')
def test():
    return "test"

__all__ = ('blueprint')