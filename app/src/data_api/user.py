import json

from flask import Blueprint, request

blueprint = Blueprint('data_user', __name__)


@blueprint.route('/user', methods=['GET'])
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

    query = "SELECT username FROM users"

    return json.dumps(
        {
            'success': True,
            'data': {
                'usernames': usnames
            }
        }
    )

@blueprint.route('/user/posts', methods=['GET'])
def posts():
    username = request.args.get('username')
    if username is None:
        return json.dumps(
            {
                'success': False,
                'reason': 'Username should be given as parameter.'
            }
        )
    # TODO lookup all post ids from a certain user
    #       and get the post_IDs
    # dummy:
    post_ID = [11, 12, 13]

    # TODO get user_id from username
    user_id = 1
    query = "SELECT id FROM posts WHERE user_id =" + user_id

    if post_ID == []:
        return json.dumps(
            {
                'success': False,
                'reason': 'User has no posts.'
            }
        )

    return json.dumps(
        {
            'success': True,
            'data': {
                'post_id': post_ID
            }
        }
    )

@blueprint.route('/post', methods=['GET'])
def post():
    post_id = request.args.get('post_id')
    if post_id is None:
        return json.dumps(
            {
                'success': False,
                'reason': 'post_id should be given as parameter.'
            }
        )

    # TODO Of the post, lookup creation date, body, title of post,
    #       username and name of creator.
    # dummy:
    creation_date='01-06-2021'
    body='some interesting text in the post that has been retrieved from the db'
    title='some interesting title'
    username='ME'
    name='creator name'

    query = "SELECT creation_date, body, title, "

    return json.dumps(
        {
            'success': True,
            'data': {
                'post_id': post_id,
                'creation_date': creation_date,
                'body': body,
                'title': title,
                'username': username,
                'name': name
            }
        }
    )

@blueprint.route('/user/details', methods=['GET'])
def details():
    username = request.args.get('username')
    if username is None:
        return json.dumps(
            {
                'success': False,
                'reason': 'username should be given as parameter.'
            }
        )

    # TODO retrieve profile details (dummy)
    # dummy:
    location='Amsterdam'
    image_url='www.google.com'
    creation_date='01-06-2021'
    study='biology'
    username='ME'
    name='creator name'

    return json.dumps(
        {
            'success': True,
            'data': {
                'username': username,
                'name': name,
                'image_url': image_url,
                'creation_date': creation_date,
                'location': location,
                'study': study,
            }
        }
    )

__all__ = ('blueprint')

