import os
from flask import Flask, jsonify, request
from app.database import init_mysql
from app.log import init_logger
from flask_cors import CORS
from app.api import init_authentication
from app.api import register_central, register_data
from app.type import get_server_type, ServerType

init_logger()
app = Flask(__name__)
app.config.from_object('config')
init_mysql(app)
init_authentication(app)
CORS(app)

def check_servertype():
    """Check the server that is supposed to be ran, change values accordingly."""
    if get_server_type() == ServerType.CENTRAL:
        from app.api.central.main import blueprint as main_routes
        app.config['JWT_TOKEN_LOCATION'] = ['cookies']
        app.config['JWT_COOKIE_CSRF_PROTECT'] = False  
        register_central(app)

    elif get_server_type() == ServerType.DATA:
        from app.api.data.main import blueprint as main_routes
        register_data(app)

    app.register_blueprint(main_routes, url_prefix='/')

    # 4 hours
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 14400

# Check servertype.
check_servertype()