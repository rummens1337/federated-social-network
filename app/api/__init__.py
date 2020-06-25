def register_data(app):
    from app.api.data.file import blueprint as data_file
    from app.api.data.friend import blueprint as data_friend
    from app.api.data.mail import blueprint as data_mail
    from app.api.data.post import blueprint as data_post
    from app.api.data.server import blueprint as data_server
    from app.api.data.user import blueprint as data_user

    app.register_blueprint(data_user, url_prefix='/api/user')
    app.register_blueprint(data_post, url_prefix='/api/post')
    app.register_blueprint(data_friend, url_prefix='/api/friend')
    app.register_blueprint(data_file, url_prefix='/api/file')
    app.register_blueprint(data_mail, url_prefix='/api/mail')
    app.register_blueprint(data_server, url_prefix='/api/server')


def register_central(app):
    from app.api.central.server import blueprint as central_server
    from app.api.central.user import blueprint as central_user

    app.register_blueprint(central_user, url_prefix='/api/user')
    app.register_blueprint(central_server, url_prefix='/api/server')


def init_authentication(app):
    # Using the expired_token_loader decorator, we will now call
    # this function whenever an expired but otherwise valid access
    # token attempts to access an endpoint
    from flask import render_template
    from flask_jwt_extended import JWTManager, jwt_required

    from app.type import get_server_type, ServerType

    jwt = JWTManager(app)

    template = 'login.html'
    if get_server_type() == ServerType.DATA:
        template = 'data/error.html'

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        return render_template(template, error='authentication')

    @jwt.unauthorized_loader
    def my_unauthorized_token_callback(expired_token):
        return render_template(template, error='authentication')

    @jwt.needs_fresh_token_loader
    def my_needs_fresh_token_loader_callback(expired_token):
        return render_template(template, error='authentication')

    @jwt.revoked_token_loader
    def my_revoked_token_loader_callback(expired_token):
        return render_template(template, error='authentication')

    @jwt.invalid_token_loader
    def my_invalid_token_loader_callback(expired_token):
        return render_template(template, error="authentication")


def auth_username():
    from flask_jwt_extended import verify_jwt_in_request_optional, \
        get_jwt_identity

    try:
        verify_jwt_in_request_optional()
        username = get_jwt_identity()
        return username
    except Exception:
        return None


def jwt_required_custom(fn):
    """
    A decorator to protect a Flask endpoint.
    If you decorate an endpoint with this, it will ensure that the requester
    has a valid and fresh access token before allowing the endpoint to be
    called.
    See also: :func:`~flask_jwt_extended.jwt_required`
    """
    import base64
    import json
    import logging

    from flask import request, current_app, Flask, render_template
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    import jwt
    import requests

    from app.type import get_server_type, ServerType
    from app.utils import get_central_ip

    def wrapper(*args, **kwargs):
        try:
            # decode token (base64)
            header = None
            if get_server_type() == ServerType.CENTRAL:
                header = request.cookies['access_token_cookie']
            else:
                header = request.headers['authorization']

            # Get the identity and save as username
            parts = header.split('.')
            decoded = base64.b64decode(parts[1] + '=============') \
                .decode('utf-8')
            username = json.loads(decoded)['identity']

            # Get the correct pub key
            if get_server_type() == ServerType.CENTRAL:
                # Get the pubkey using own API call
                from app.api.central.server import get_pub_key
                pub = get_pub_key(username)
            else:
                # Get the pubkey by call to the central server
                pub = requests.get(
                    get_central_ip() + '/api/server/pub_key',
                    params={
                        'username': username
                    }
                ).json()['data']

            current_app.config['JWT_PUBLIC_KEY'] = pub
        except:
            # Show login on exception
            return render_template('login.html')

        # Let the JWT extended library check the token
        verify_jwt_in_request()
        return fn(*args, **kwargs)

    wrapper.__name__ = fn.__name__
    return wrapper

