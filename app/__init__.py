import os

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token
)
from app.database import init_mysql
from app.log import init_logger

init_logger()
app = Flask(__name__)
app.config.from_object('config')
init_mysql(app)

from app.api import register_central, register_data
from app.type import get_server_type, ServerType

# TODO is this only needed for data / central? if so: move it inside the IF.

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)
# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401

@jwt.unauthorized_loader
def my_unauthorized_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token can not be authorized'.format(token_type)
    }), 401

@jwt.needs_fresh_token_loader
def my_needs_fresh_token_loader_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token needs to be refreshed'.format(token_type)
    }), 401

@jwt.revoked_token_loader
def my_revoked_token_loader_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has been revoked'.format(token_type)
    }), 401


if get_server_type() == ServerType.CENTRAL:
    from app.api.central.main import blueprint as main_routes
    register_central(app)

elif get_server_type() == ServerType.DATA:
    from app.api.data.main import blueprint as main_routes
    register_data(app)

app.register_blueprint(main_routes, url_prefix='/')

