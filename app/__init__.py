import os

from flask import Flask, jsonify, request
from app.database import init_mysql
from app.log import init_logger

from flask_cors import CORS
from app.api import init_authentication

init_logger()
app = Flask(__name__)
app.config.from_object('config')
init_mysql(app)
init_authentication(app)
CORS(app)

from app.api import register_central, register_data
from app.type import get_server_type, ServerType


if get_server_type() == ServerType.CENTRAL:
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    from app.api.central.main import blueprint as main_routes
    register_central(app)

elif get_server_type() == ServerType.DATA:
    from app.api.data.main import blueprint as main_routes
    register_data(app)

app.register_blueprint(main_routes, url_prefix='/')

