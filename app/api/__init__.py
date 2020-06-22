def register_data(app):
    from app.api.data.user import blueprint as data_user
    from app.api.data.post import blueprint as data_post
    from app.api.data.friend import blueprint as data_friend
    from app.api.data.file import blueprint as data_file
    from app.api.data.mail import blueprint as data_mail
    from app.api.data.server import blueprint as data_server
    app.register_blueprint(data_user, url_prefix='/api/user')
    app.register_blueprint(data_post, url_prefix='/api/post')
    app.register_blueprint(data_friend, url_prefix='/api/friend')
    app.register_blueprint(data_file, url_prefix='/api/file')
    app.register_blueprint(data_mail, url_prefix='/api/mail')
    app.register_blueprint(data_server, url_prefix='/api/server')


def register_central(app):
    from app.api.central.user import blueprint as central_user
    from app.api.central.server import blueprint as central_server
    app.register_blueprint(central_user, url_prefix='/api/user')
    app.register_blueprint(central_server, url_prefix='/api/server')


def init_authentication(app):
    # Using the expired_token_loader decorator, we will now call
    # this function whenever an expired but otherwise valid access
    # token attempts to access an endpoint
    from flask_jwt_extended import JWTManager, jwt_required
    from flask import render_template
    from app.type import get_server_type, ServerType
    jwt = JWTManager(app)

    template = "login.html"
    if get_server_type() == ServerType.DATA:
        template = "data/error.html"

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        return render_template(template, error="authentication")

    @jwt.unauthorized_loader
    def my_unauthorized_token_callback(expired_token):
        return render_template(template, error="authentication")

    @jwt.needs_fresh_token_loader
    def my_needs_fresh_token_loader_callback(expired_token):
        return render_template(template, error="authentication")

    @jwt.revoked_token_loader
    def my_revoked_token_loader_callback(expired_token):
        return render_template(template, error="authentication")

def auth_username():
    from flask_jwt_extended import verify_jwt_in_request_optional, get_jwt_identity
    try:
        verify_jwt_in_request_optional()
        username = get_jwt_identity()
        return username
    except Exception:
        return None
