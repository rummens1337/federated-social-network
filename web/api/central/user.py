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

__all__ = ('blueprint')

