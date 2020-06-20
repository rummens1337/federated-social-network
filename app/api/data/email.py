from flask_mail import Message
from flask import Blueprint, request
from flask_mail import Mail
import flask

blueprint = Blueprint('data_email', __name__)

@blueprint.route("/")
def index():


    msg = Message("Hello",
                  sender="michelrummens@hotmail.com",
                  recipients=["michelrummens@hotmail.com.com"])
    mail.send(msg)