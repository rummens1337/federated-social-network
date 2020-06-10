import os

from flask import Flask

from app.database import init_mysql
from app.log import init_logger

init_logger()
app = Flask(__name__)
app.config.from_object('config')
init_mysql(app)

from app.api import register_central, register_data
from app.utils import server_type

if server_type() == 'CENTRAL':
    from app.api.central.main import blueprint as main_routes
    register_central(app)
elif server_type() == 'DATA':
    from app.api.data.main import blueprint as main_routes
    register_data(app)

app.register_blueprint(main_routes, url_prefix='/')