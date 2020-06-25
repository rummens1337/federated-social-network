from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.api import jwt_required_custom
from app.api.utils import good_json_response, bad_json_response
from app.database import users, posts, comments, uploads
from app.upload import get_file, save_file
from app.utils import ping, get_central_ip, get_own_ip, get_user_ip

blueprint = Blueprint('data_post', __name__)


# TODO COMMENTS
@blueprint.route('/', strict_slashes=False)
@jwt_required_custom
def post():
    # TODO user should be authenticated

    post_id = request.args.get('post_id')

    if post_id is None:
        return bad_json_response('post_id should be given as parameter.')

    post_db = posts.export('id', id=post_id)
    if not post_db:
        return bad_json_response('post not found')

    post_db = posts.export('body', 'title', 'username', 'uploads_id',
                           'creation_date', 'last_edit_date', id=post_id)[0]

    # Get image
    up_id = post_db[3]
    imageurl = ''
    if uploads.exists(id=up_id):
        filename = uploads.export_one('filename', id=up_id)
        imageurl = get_own_ip() + 'file/{}/{}'.format(up_id, filename)

    return good_json_response({
        'post_id': post_id,
        'body': post_db[0],
        'title': post_db[1],
        'username': post_db[2],
        'image_url': imageurl,
        'creation_date': str(post_db[4]),
        'last_edit_date': str(post_db[5])
    })


@blueprint.route('/create', methods=['POST'])
@jwt_required_custom
def create():
    username = get_jwt_identity()
    title = request.form['title']
    body = request.form['body']
    # username = request.form['username']


    # TODO fail if user is not registered
    # TODO user should be authenticated

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
    if 'file' in request.files:
        image_filename = request.files['file'].filename
        image = request.files['file'].read()

        if image is not 0:
            uploads_id = save_file(image, filename=image_filename)

            if uploads_id is not False:
                posts.insert(
                    username=username, body=body, title=title,
                    uploads_id=uploads_id
                    )
    else:
        posts.insert(username=username, body=body, title=title)

    return good_json_response('success')


@blueprint.route('/delete', methods=['POST'])
@jwt_required_custom
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
    posts.delete(id=post_id)

    return good_json_response('success')


# @blueprint.route('/uploadPost', methods=['POST'])
# @jwt_required
# def uploadPost():
#     username = get_jwt_identity()
#     # username = request.form['username']

#     image_filename = request.files['file'].filename
#     image = request.files['file'].read()

#     if image is not 0:
#         uploads_id = save_file(image, filename=image_filename)

#     if uploads_id is not False:
#         posts.update({'uploads_id' : uploads_id}, username=username)


@blueprint.route('/getComments')
# @jwt_required
def getComments():
    post_id = request.args.get('post_id')

    if post_id is None or post_id == '':
        return bad_json_response(
            "Bad request: Missing or invalid parameter 'post_id'."
        )

    if not posts.exists(id=post_id):
        return bad_json_response('Post id does not exist.')

    comment_details = comments.export('id', 'comment', 'username',
                                      'creation_date', 'last_edit_date',
                                      post_id=post_id)

    comments_array = [
        {
            'id': item[0],
            'comment': item[1],
            'username': item[2],
            'creation_date': str(item[3]),
            'last_edit_date': str(item[4])
        }
        for item in comment_details
    ]

    return good_json_response({
        'comments': comments_array
    })


@blueprint.route('/addComment', methods=['POST'])
@jwt_required_custom
def addComment():
    username = get_jwt_identity()
    # username = request.form['username']

    # need to somehow give post_id with it (in html? hidden)
    post_id = int(request.form['post_id'])
    comment = request.form['comment']

    comments.insert(comment=comment, post_id=post_id, username=username)

    return good_json_response('success')


@blueprint.route('/editComment', methods=['POST'])
# @jwt_required
def editComment():
    # username = get_jwt_identity()
    # username = request.form['username']

    id = request.form['id']
    comment = request.form['comment']

    comments.update({'comment': comment}, id=id)

    return good_json_response('success')


@blueprint.route('/deleteComment', methods=['POST'])
# @jwt_required
def deleteComment():
    id = request.form['id']

    comments.delete(id=id)

    return good_json_response('success')


__all__ = ('blueprint',)
