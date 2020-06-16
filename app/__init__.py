import os

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token
)
from app.database import init_mysql
from app.log import init_logger

from flask_cors import CORS
from flask import render_template


init_logger()
app = Flask(__name__)
app.config.from_object('config')
init_mysql(app)
CORS(app)

from app.api import register_central, register_data
from app.type import get_server_type, ServerType

# TODO is this only needed for data / central? if so: move it inside the IF.

jwt = JWTManager(app)
# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    return render_template("error.html", error="authentication")

@jwt.unauthorized_loader
def my_unauthorized_token_callback(expired_token):
    return render_template("error.html", error="authentication")

@jwt.needs_fresh_token_loader
def my_needs_fresh_token_loader_callback(expired_token):
    return render_template("error.html", error="authentication")

@jwt.revoked_token_loader
def my_revoked_token_loader_callback(expired_token):
    return render_template("error.html", error="authentication")


if get_server_type() == ServerType.CENTRAL:
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    from app.api.central.main import blueprint as main_routes
    register_central(app)

elif get_server_type() == ServerType.DATA:
    from app.api.data.main import blueprint as main_routes
    register_data(app)

app.register_blueprint(main_routes, url_prefix='/')

