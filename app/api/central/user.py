from flask import Blueprint, request, Flask, render_template, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/', methods=['GET'])
def user():
    # TODO get list of usernames from database
    # dummy:

    users.insert(username='testuser', address='0.0.0.0:9000')
    usernames = users.export('username', 'address')

    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/address', methods=['GET'])
def address():
    username = request.args.get('username')
    print(username)

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO fail if user is not registered

    address = users.export_one('address', username=username)

    return good_json_response({
        'address': address
    })


@blueprint.route('/registered', methods=['GET'])
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


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    # username = request.form['username']
    # address = request.form['address']
    username = request.args.get('username')
    address = request.args.get('address')

    users.insert(username=username, address=address)

    return good_json_response()


@blueprint.route('/delete', methods=['POST', 'GET'])
def delete():
    #username = request.form['username']
    username = request.args.get('username')

    # TODO fail if user is not registered

    users.delete(username=username)

    return good_json_response()


@blueprint.route('/edit', methods=['POST', 'GET'])
def edit():
    #username = request.form['username']
    username = request.args.get('username')

    # TODO fail if user is not registered

    if 'new_address' in request.form:
        # TODO replace address
        #new_address = request.form['address']
        new_address=request.args.get('new_address')
        query = "UPDATE users SET address = " + new_address + "WHERE username = " + username
        pass
    if 'new_username' in request.form:
        # TODO replace username
        # new_username = request.form['new_username']
        new_username = request.args.get('new_username')
        query = "UPDATE users SET username = " + new_username + "WHERE username = " + username

    if 'address' in request.form:
        # TODO replace address

        pass

    return good_json_response()

__all__ = ('blueprint')

