from flask import Flask
import os

from app.database import init_mysql
app = Flask(__name__)
app.config.from_object('config')
init_mysql(app)

from app.api import register_central, register_data
from app.main import blueprint as main_routes
from app.utils import server_type

app.register_blueprint(main_routes, url_prefix='/')

if server_type() == 'CENTRAL':
    register_central(app)
elif server_type() == 'DATA':
    register_data(app)

