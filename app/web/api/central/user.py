import json

from flask import Blueprint, request

blueprint = Blueprint('central_user', __name__)


@blueprint.route('/address')
def address():
    username = request.args.get('username')
    if username is None:
        return json.dumps(
            {
                'success': False,
                'reason': 'Username should be given as parameter.'
            }
        )
    # TODO get address from database
    # dummy:
    address = '0.0.0.0'
    return json.dumps(
        {
            'success': True,
            'data': {
                'address': address
            }
        }
    )

@blueprint.route('/')
def user():
    # TODO get list of usernames from database
    # dummy:
    usnames = ['user1', 'user2', 'user3']
    if usnames == []:
        return json.dumps(
            {
                'success': False,
                'reason': 'No usernames in the database.'
            }
        )

    return json.dumps(
        {
            'success': True,
            'data': {
                'usernames': usnames
            }
        }
    )

@blueprint.route('/registered')
def registered():
    username = request.args.get('username')
    if username is None:
        return json.dumps(
            {
                'success': False,
                'reason': 'Username should be given as parameter.'
            }
        )

    # TODO look if username exists in database
    # dummy:
    usnamecheck = 'exists'

    if username == usnamecheck:
        return json.dumps(
            {
                'success': True,
                'data': {
                    'registered': 'TRUE'
                }
            }
        )

    return json.dumps(
            {
                'success': False,
                'data': {
                    'registered': 'FALSE'
                }
            }
        )

@blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    address = request.form['address']

    # TODO insert entry for username and address in datatbase.

    # This is just for testing.
    return json.dumps(
        {
            'success': True,
            'data': {
                'username': username,
                'address': address
            }
        }
    )


__all__ = ('blueprint')

