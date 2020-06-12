from flask import Blueprint, request, Flask, render_template, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/')
def user():
    # TODO get list of usernames from database
    # dummy:

    users.insert(username='user1', address='address1')
    users.insert(username='user2', address='address2')
    users.insert(username='user3', address='address3')
    usernames = users.export('username', 'address')
    users.delete(username='user1')
    users.delete(username='user2')
    users.delete(username='user3')

    # usernames = ['user1central', 'user2central']


    if len(usernames) == 0:
        return bad_json_response('No usernames in the database.')

    return good_json_response({
        'usernames': usernames
    })


@blueprint.route('/address')
def address():
    username = request.form['username']

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO fail if user is not registered

    address = users.export_one('address', username=username)

    return good_json_response({
        'address': address
    })


@blueprint.route('/registered')
def registered():
    username = request.args.get('username')

    if username is None:
        return bad_json_response('Username should be given as parameter.')

    # TODO look if username exists in database
    exists = users.exists()

    return good_json_response({
        'registered': exists
    })


@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    address = request.form['address']

    if '@' not in address:
        return bad_json_response('Invalid e-mail address.')

    users.insert(username=username, address=address)

    return good_json_response()


@blueprint.route('/delete', methods=['POST'])
def delete():
    username = request.form['username']

    # TODO fail if user is not registered

    users.delete(username=username)

    return good_json_response()


@blueprint.route('/edit', methods=['POST'])
def edit():
    username = request.form['username']

    # TODO fail if user is not registered

    if 'new_address' in request.form:
        new_address = request.form['new_address']
        # TODO update in database
        users.update()
    if 'new_username' in request.form:
        new_username = request.form['new_username']
        # TODO update in database
        users.update()

    return good_json_response()

__all__ = ('blueprint')

