appp = None

def register_data(app):
    appp = app
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

def custom_jwt_required(fn):
    """
    A decorator to protect a Flask endpoint.
    If you decorate an endpoint with this, it will ensure that the requester
    has a valid and fresh access token before allowing the endpoint to be
    called.
    See also: :func:`~flask_jwt_extended.jwt_required`
    """
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    from flask import request, current_app, Flask
    # from app.database import servers

    # app = Flask(__name__)

    # import logging

    # with current_app.app_context():
    #     logging.debug(get_jwt_identity()) 



    # @wraps(fn)
    def wrapper(*args, **kwargs):
        import logging


        

        token = request.headers['authorization']

        # decode token (base64)
        # read u = token_decoded['identity']  THIS IS THE USENAME
        # get public key uing centralSserver/api/user/address?username=u
        # set public key like this:

        current_app.config['JWT_PUBLIC_KEY'] = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAmUKUAi3m3DdHX4YfHnVl
0ePaqEgKE02ZijFTpB+y71ZqpDYzTql06XSVkk8O3Ylbwc5GSH5sJS7bQlhoKTWy
4A0rSaJP4n5AQ2pNKjkZbMDrylglQx4AHxPe0b6hIvLAiW8ZKSyLVaY+kH1+GdWR
/ggE7n/MCnyOT4/4fyWvl6Wyiw9r2orqrcjYPpkgpQjbOdJRKBJ+iXNzUYV85VZY
vfwERJhmIJabDr9BmsKwNksRsRzdBkO6QTkrTfIykM0fBz57ZZJyjYxNBLviZzPr
09ulO8vmA2i8TMdOcFbOIhD9CrmQIWbHpruksuMYE5ea1RDfAulV5gaMHn6FuHDl
RURD3bmQ4qGteu74tlabuQoTwfR4Jg5VoRfjWLxOL5H/mLWZOla05thai3ci32fO
RECrvB9BFh1vz8YPsljgAd5Kmmv9E0x3aIgJHkoFaQR0lMQ5BFop5bOglHJ3Lbqh
MjBwxP0f2Hyock7zM75J5b72/G4Ua+OYZBwlgSucr+bW7fsjx33vp9L7+9WD/HCt
tDYOJ1AwmLqVxeGSsRgNVxNSgKIgZqmgtXtWVuX5Ta8g4DU+lb3/966s5c/FuMbR
vFWNZ2eysczAxCfg64C3Ze2nzKHGbQ1mMA+eNZ1decJVUU3j06/mzoyj/LvXIzht
27ApYiuikwDI5JxkLR0NyBkCAwEAAQ==
-----END PUBLIC KEY-----"""

        url = request.url_root
        # pub_key = servers.export('pub_key', address=url)

        
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper