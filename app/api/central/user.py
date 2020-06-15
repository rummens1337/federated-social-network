from flask import Blueprint, request, Flask, render_template, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/', methods=['GET'])
def user():
    usernames = users.export('username', 'address')

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
    usernames = ['nick', 'auke']
    address = '0.0.0.0:9000/'
    for username in usernames:
        users.insert(username=username, address=address)
    return good_json_response()
    # TODO error handling if query fails


@blueprint.route('/address', methods=['GET'])
def address():
    username = request.form['username']

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    if users.exists(username=username):
        address = users.export_one('address', username=username)

        return good_json_response({
            'address': address
        })
    else:
        return bad_json_response('Username does not exist in database.')


@blueprint.route('/registered', methods=['GET'])
def registered():
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
    address = request.form['address']

    if '@' not in address:
        return bad_json_response('Invalid e-mail address.')

    users.insert(username=username, address=address)

    return good_json_response()
    # TODO error handling if query fails


@blueprint.route('/delete', methods=['POST'])
def delete():
    username = request.form['username']

    if users.exists(username=username):
        users.delete(username=username)
        return good_json_response()
    else:
        return bad_json_response("Username does not exist in database.")
    # TODO error handling if query fails


@blueprint.route('/edit', methods=['POST'])
def edit():
    username = request.args.get('username')

    if users.exists(username=username):
        if 'new_address' in request.form:
            new_address = request.form['new_address']
            if 'new_address' != '':
                users.update({'address':new_address}, username=username)
        if 'new_username' in request.form:
            new_username = request.form['new_username']
            if 'new_username' != '':
                users.update({'username':new_username}, username=username)
    else:
        return bad_json_response('Username does not exist in database.')

    return good_json_response()
    # TODO error handling if query fails

__all__ = ('blueprint')
