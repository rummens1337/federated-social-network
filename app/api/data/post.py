from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response

blueprint = Blueprint('data_post', __name__)


@blueprint.route('/')
def post():
    post_id = request.args.get('post_id')

    if post_id is None:
        return bad_json_response('post_id should be given as parameter.')

    # TODO fail if post is not found

    # TODO Of the post, lookup creation date, body, title of post,
    #       username and name of creator.
    # dummy:
    creation_date='01-06-2021'
    body='some interesting text in the post that has been retrieved from the db'
    title='some interesting title'
    username='ME'
    name='creator name'

    return good_json_response({
        'post_id': post_id,
        'creation_date': creation_date,
        'body': body,
        'title': title,
        'username': username,
        'name': name
    })


@blueprint.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    title = request.form['title']
    body = request.form['body']

    # TODO fail if user is not registered

    # TODO create new post in database

    # TODO get URL of post
    # dummy:
    url = 'https://google.com'

    return good_json_response({
        'url': url
    })


@blueprint.route('/delete', methods=['POST'])
def delete():
    post_id = request.form['post_id']

    # TODO fail if post is not registered

    # TODO delete post from database

    return good_json_response()

__all__ = ('blueprint')

