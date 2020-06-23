from flask import Blueprint, request

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.database import posts, comments

blueprint = Blueprint('data_post', __name__)

# TODO COMMENTS

@blueprint.route('/', strict_slashes=False)
@jwt_required
def post():
    # TODO user should be authenticated

    post_id = request.args.get('post_id')

    if post_id is None:
        return bad_json_response('post_id should be given as parameter.')

    post_db = posts.export('id', id=post_id)
    if not post_db:
        return bad_json_response('post not found')

    post_db = posts.export('body', 'title', 'username', 'creation_date', 'last_edit_date', id=post_id)[0]

    return good_json_response({
        'post_id': post_id,
        'body': post_db[0],
        'title': post_db[1],
        'username': post_db[2],
        'creation_date': str(post_db[3]),
        'last_edit_date': str(post_db[4])
    })


@blueprint.route('/create', methods=['POST'])
@jwt_required
def create():
    username = get_jwt_identity()
    title = request.form['title']
    body = request.form['body']

    # TODO fail if user is not registered
    # TODO user should be authenticated

    # TODO get URL of post
    # dummy:
    url = '/api/post/XX'

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")
    if title is None:
        return bad_json_response("Bad request: Missing parameter 'title'.")
    if body is None:
        return bad_json_response("Bad request: Missing parameter 'body'.")

    # check if user id exists
    if not users.exists(username=username):
        return bad_json_response('User not found.')

    # Insert post
    posts.insert(username=username, body=body, title=title)

    return good_json_response({
        'url': url
    })

@blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    username = get_jwt_identity()
    post_id = request.form['post_id']

    if username is None:
        return bad_json_response("Bad request: Missing parameter 'username'.")
    if post_id is None:
        return bad_json_response("Bad request: Missing parameter 'post_id'.")

    # check if user id exists
    if not users.exists(username=username):
        return bad_json_response('User not found')

    # check if post id exists
    if not posts.exists(id=post_id):
        return bad_json_response('Post not found')

    # Check if the user is the post owner
    post_username = posts.export_one('username', id=post_id)
    if post_username != username:
        return bad_json_response('Not your post')

    # Delete post
    posts.delete(id = post_id)

    return good_json_response("success")


# @blueprint.route('/uploadPost', methods=['POST'])
# @jwt_required
# def uploadPost():
#     image_filename = request.files['file'].filename
#     image = request.files['file'].read()

#     if image is not 0:
#         uploads_id = save_file(image, filename=image_filename)

#     if uploads_id is not False:
#         users.update({'uploads_id' : uploads_id}, username=username)


@blueprint.route('/getcomments')
# @jwt_required
def getcomments():
    post_id = request.args.get('post_id')

    if post_id is None or post_id == '':
        return bad_json_response(
                "Bad request: Missing or invalid parameter 'post_id'."
                )

    comment_details = comments.export(
            'id', 'comment', 'creation_date',
            'last_edit_date', post_id=post_id
            )

    comments_array = [{
            'id': item[0],
            'comment': item[1],
            'creation_date': str(item[2]),
            'last_edit_date': str(item[3])
        }
        for item in comment_details
    ]

    return good_json_response({
        'comments': comments_array
    })


# @blueprint.route('/addComment', methods=['POST'])
# @jwt_required
# def addComment():
#     username = get_jwt_identity()
#     # need to somehow give post_id with it (in html?)
#     post_id = request.form['post_id']
#     comment = request.form['comment']

#     comments.insert(comment=comment, post_id=post_id)



__all__ = ('blueprint')

