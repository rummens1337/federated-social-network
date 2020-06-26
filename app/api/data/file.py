"""
This file contains a file handler for the data server.
"""

from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response
from app.database import uploads

blueprint = Blueprint('data_file', __name__)


@blueprint.route('/', strict_slashes=False)
def file_main():
    """Function that handles getting a file.

    Returns:
        A bad JSON response if file is not found.
        A good JSON response with file URL if file is found successfully
    """
    file_id = request.args.get('id')

    if not uploads.exists(id=file_id):
        return bad_json_response('File ID does not exist.')

    filename = uploads.export_one('filename', id=file_id)

    return good_json_response({
        'url': '/file/{}/{}'.format(file_id, filename)
    })


__all__ = ('blueprint',)
