from flask import Flask
import os

from app.api import register_central, register_data
from app.database import init_mysql
from app.main import blueprint as main_routes

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(main_routes, url_prefix='/')
init_mysql(app)

if os.environ['SERVER_TYPE'] == 'CENTRAL':
    register_central(app)
elif os.environ['SERVER_TYPE'] == 'DATA':
    register_data(app)
else:
    # Loads central if not specified or wrong
    register_central(app)