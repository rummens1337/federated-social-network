from web.api.central.user import blueprint as user_blueprint


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/api/user')

__all__ = ('register_blueprints')

