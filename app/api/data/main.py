"""
This file contains all URL routes for data servers.
"""

import mimetypes

from flask import render_template, flash, redirect, session, url_for, request, \
    g, Markup, Blueprint, send_file

from app.api.utils import good_json_response, bad_json_response
from app.database import test_db, uploads
from app.upload import get_file

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return 'DATA SERVER'


@blueprint.route('/ping')
def ping():
    return good_json_response()


@blueprint.route('/file/<int:file_id>/<filename>')
def file(file_id: int, filename: str):
    if not uploads.exists(id=file_id, filename=filename):
        return bad_json_response('File ID and/or filename does not exist.')
    return send_file(get_file(file_id, output='fp')[1],
                     mimetype=mimetypes.guess_type(filename)[0])


__all__ = ('blueprint',)
