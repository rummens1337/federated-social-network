"""
This file contains api routes corresponding to server information
on a data server.
"""

from flask import Blueprint, request, Flask, render_template, request
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.api.utils import good_json_response, bad_json_response
from app.utils import get_own_ip

blueprint = Blueprint('data_server', __name__)


@blueprint.route('/pub_key')
def get_key():
    """Function for getting the public key.

    Returns:
        JSON reponse with either public key on success or error message on
        failure.
    """
    with open('jwtRS256.key.pub') as f:
        pub_key = f.read()

    if pub_key is not None:
        return good_json_response(pub_key)
    else:
        return bad_json_response(
            'Error retrieving the public key of server: ' + get_own_ip()
        )


__all__ = ('blueprint',)
