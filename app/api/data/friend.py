from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response

blueprint = Blueprint('data_friend', __name__)


@blueprint.route('/add', methods=['POST'])
def register():
    username = request.form['username']
    friend_username = request.form['friend_username']

    # TODO fail if friend_username or username does not exist

    # TODO register friendship in database

    return good_json_response()


@blueprint.route('/delete', methods=['POST'])
def delete():
    username = request.form['username']
    friend_username = request.form['friend_username']

    # TODO fail if friend_username or username does not exist

    # TODO delete friendship from database

    return good_json_response()

__all__ = ('blueprint')

