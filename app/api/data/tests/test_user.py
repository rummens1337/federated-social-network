from flask import Blueprint, request

from app.api.utils import good_json_response, bad_json_response

blueprint = Blueprint('data_user', __name__)


# blueprint.route('/')
def test_user():
	pass


# blueprint.route('/posts')
def test_posts():
	pass


# blueprint.route('/details')
def test_details():
    pass


# blueprint.route('/register', methods=['POST'])
def test_register():
    pass


# blueprint.route('/delete', methods=['POST'])
def delete():
    pass


# blueprint.route('/edit', methods=['POST'])
def test_edit():
    pass

__all__ = ('blueprint')

