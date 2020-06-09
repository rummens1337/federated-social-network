from flask import Blueprint, request, Flask, render_template, request

from app.api.utils import good_json_response, bad_json_response

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/')
def user():
    # TODO get list of usernames from database
    # dummy:
    usernames = ['user1', 'user2', 'user3']

    query = "SELECT username FROM users"

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/address')
def address():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO fail if user is not registered

    # TODO get address from database
    # dummy:
    address = '0.0.0.0'

    query = "SELECT address FROM users WHERE username = " + username

    return good_json_response({
        'address': address
    })


@blueprint.route('/registered')
def registered():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO look if username exists in database

    "SELECT address from users WHERE username = " + username
    # TODO check length of result > 0

    return good_json_response({
        'registered': username == usnamecheck
    })


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    address = request.form['address']

    if '@' not in address:
        return bad_json_response('Invalid e-mail address.')

    # TODO insert entry for username and address in datatbase.
    query = "INSERT INTO users (username, address) VALUES (" + username + ", " + address + ")"

    return good_json_response()


@blueprint.route('/delete', methods=['POST'])
def delete():
    username = request.form['username']

    # TODO fail if user is not registered

    # TODO delete user

    query = "DELETE FROM users WHERE username = " + username

    return good_json_response()


@blueprint.route('/edit', methods=['POST'])
def edit():
    username = request.form['username']

    # TODO fail if user is not registered

    if 'address' in request.form:
        # TODO replace address
        new_address = request.form['address']
        query = "UPDATE users SET address = " + new_address + "WHERE username = " + username
        pass
    if 'new_username' in request.form:
        # TODO replace username
        new_username = request.form['new_username']
        query = "UPDATE users SET username = " + new_username + "WHERE username = " + username
        pass

    return good_json_response()

__all__ = ('blueprint')

