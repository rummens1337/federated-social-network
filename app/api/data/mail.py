import smtplib
from email.message import EmailMessage
from flask import Blueprint, request, url_for, Flask
import email, smtplib, ssl
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import current_app
from app.database import users
from app.api.utils import good_json_response, bad_json_response

blueprint = Blueprint('data_mail', __name__)

@blueprint.route('/token/<send_to>', methods=['GET', 'POST'])
def send_verification_mail(send_to):
    # Construct message object with receipient and sender
    msg = EmailMessage()
    msg['Subject'] = 'FedNet - Please verify your email!'
    msg['From'] = current_app.config['EMAIL_ADDRESS']
    msg['To'] = send_to

    # Create the secret key based on our little secret :)
    secret = URLSafeTimedSerializer(current_app.config['EMAIL_SECRET'])

    # Create token based on a user their email and salt to prevent same token.
    token = secret.dumps(send_to, salt=current_app.config['EMAIL_SALT'])

    # Create link with token and add it to the body of the mail.
    link = url_for('data_mail.confirm_email', token=token, _external=True)
    msg.add_alternative('Your link is {}'.format(link), subtype="plaintext")

    # TODO: add link in template below!
    # verify_file = open('app/api/data/verify-mail.html')
    # html = verify_file.read()
    # msg.add_alternative(html, subtype='html')

    # Connect to the mailserver from google and send the e-mail.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(current_app.config['EMAIL_ADDRESS'], current_app.config['EMAIL_PASSWORD'])
        smtp.send_message(msg)
    
    # TODO: If success give user a pop-up in the front-end.  
    return True
    # return '<h1>The email you entered is {}. The token is </h1>'.format(token)

@blueprint.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        # Create the secret key based on our little secret :)
        secret = URLSafeTimedSerializer(current_app.config['EMAIL_SECRET'])

        # Confirm key is in pool and has not expired yet.
        email = secret.loads(token, salt=current_app.config['EMAIL_SALT'], max_age=3600)

        if users.exists(email=email):
            users.update({'email_confirmed':1}, email=email)
            return good_json_response("successfully registered for email " + email)
        else:
            return bad_json_response("No user with the email " + email + " exists.")
    except SignatureExpired:
        return bad_json_response("The token has expired. Please try registering again.")
