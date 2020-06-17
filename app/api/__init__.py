def register_data(app):
    from app.api.data.user import blueprint as data_user
    from app.api.data.post import blueprint as data_post
    from app.api.data.friend import blueprint as data_friend
    app.register_blueprint(data_user, url_prefix='/api/user')
    app.register_blueprint(data_post, url_prefix='/api/post')
    app.register_blueprint(data_friend, url_prefix='/api/friend')


def register_central(app):
    from app.api.central.user import blueprint as central_user
    app.register_blueprint(central_user, url_prefix='/api/user')


def init_authentication(app):
    # Using the expired_token_loader decorator, we will now call
    # this function whenever an expired but otherwise valid access
    # token attempts to access an endpoint
    from flask_jwt_extended import JWTManager, jwt_required
    from flask import render_template
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        return render_template("login.html", error="authentication")

    @jwt.unauthorized_loader
    def my_unauthorized_token_callback(expired_token):
        return render_template("login.html", error="authentication")

    @jwt.needs_fresh_token_loader
    def my_needs_fresh_token_loader_callback(expired_token):
        return render_template("login.html", error="authentication")

    @jwt.revoked_token_loader
    def my_revoked_token_loader_callback(expired_token):
        return render_template("login.html", error="authentication")