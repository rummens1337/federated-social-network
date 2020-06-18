from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import posts

blueprint = Blueprint('data_post', __name__)

# TODO COMMENTS

@blueprint.route('/', methods=['POST'])
def search():
    input_data = request.form['search_input']

    # TODO fail if user is already registered
    if users.exists(username=username):
        return bad_json_response('Username is already registered.')

    # TODO register user and save image | still todo save image
    users.insert(username=username, location=location, study=study)

    return good_json_response("success")