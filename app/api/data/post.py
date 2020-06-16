from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import posts

blueprint = Blueprint('data_post', __name__)

# TODO COMMENTS

@blueprint.route('/', strict_slashes=False)
def post():
    # TODO user should be authenticated

    post_id = request.args.get('post_id')

    if post_id is None:
        return bad_json_response('post_id should be given as parameter.')

    post_db = posts.export('id', id=post_id)
    if not post_db:
        return bad_json_response('post not found')

    post_db = posts.export('body', 'title', 'users_id', 'creation_date', 'last_edit_date', id=post_id)[0]

    return good_json_response({
        'post_id': post_id,
        'body': post_db[0],
        'title': post_db[1],
        'user_id': post_db[2],
        'creation_date': str(post_db[3]),
        'last_edit_date': str(post_db[4])
    })


@blueprint.route('/create', methods=['POST'])
def create():
    user_id = request.form['user_id']
    title = request.form['title']
    body = request.form['body']

    # TODO fail if user is not registered
    # TODO user should be authenticated

    # TODO get URL of post
    # dummy:
    url = '/api/post/XX'

    if user_id is None:
        return bad_json_response('User_id should be given as parameter.')
    if title is None:
        return bad_json_response('Title should be given as parameter.')
    if body is None:
        return bad_json_response('Body should be given as parameter.')

    # check if user id exists
    if not users.exists(id=user_id):
        return bad_json_response('user not found')

    # Insert post
    posts.insert(users_id=str(user_id), body=body, title=title)

    return good_json_response({
        'url': url
    })

@blueprint.route('/delete', methods=['POST'])
def delete():
    user_id = request.form['user_id']
    post_id = request.form['post_id']

    # TODO user should be authenticated
    # TODO authenticated user should be the post owner

    if user_id is None:
        return bad_json_response('user_id should be given as parameter.')
    if post_id is None:
        return bad_json_response('Post_id should be given as parameter.')

    # check if user id exists
    if not users.exists(id=user_id):
        return bad_json_response('User not found')

    # check if post id exists
    if not posts.exists(id=post_id):
        return bad_json_response('Post not found')

    # Delete post
    posts.delete(id = post_id)

    return good_json_response()


__all__ = ('blueprint')

