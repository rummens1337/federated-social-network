from app.api.central.user import blueprint as central_user
from app.api.data.user import blueprint as data_user
from app.api.data.post import blueprint as data_post


def register_data(app):
    app.register_blueprint(data_user, url_prefix='/api/user')
    app.register_blueprint(data_post, url_prefix='/api/post')
    app.register_blueprint(data_friend, url_prefix='/api/friend')


def register_central(app):
    app.register_blueprint(central_user, url_prefix='/api/user')

