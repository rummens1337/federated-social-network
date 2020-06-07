from flask import Flask

from app.api import register_central, register_data
from app.database import init_mysql
from app.main import blueprint as main_routes

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(main_routes, url_prefix='/')
init_mysql(app)


def run_base(port: int):
    app.run(host='0.0.0.0', port=port)


def run_central(*args):
    register_central(app)
    run_base(*args)


def run_data():
    register_data(app)
    run_base(*args)

