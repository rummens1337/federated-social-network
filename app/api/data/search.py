"""
This file contains api routes corresponding to searching 
on a data server.
"""

from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users, posts

blueprint = Blueprint('data_post', __name__)


@blueprint.route('/', methods=['POST'])
def search():
    input_data = request.form['search_input']

    if users.exists(username=username):
        return bad_json_response('Username is already registered.')

    users.insert(username=username, location=location, study=study)

    return good_json_response('success')


__all__ = ('blueprint',)
