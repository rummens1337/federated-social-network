from email.message import EmailMessage
from email.utils import make_msgid
import email
import mimetypes
import smtplib
import ssl

from flask import Blueprint, request, url_for, Flask, current_app, redirect
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, \
    BadTimeSignature
from passlib.hash import sha256_crypt

from app.api.utils import good_json_response, bad_json_response
from app.database import users
from app.utils import get_central_ip, get_own_ip

blueprint = Blueprint('data_mail', __name__)


@blueprint.route('/token', methods=['POST'])
def send_verification_mail():
    # Check if parameter email is set.
    send_to = request.form['email']
    if not send_to:
        return bad_json_response("Bad request: Missing parameter 'email'.")

    # Retrieve user from server for personal message in email.
    user = users.export_one('firstname', 'lastname',
                            email=request.form['email'])

    # If no user is found give an error.
    if not user:
        return bad_json_response('Error retrieving the user.')

    # Construct message object with receipient and sender
    msg = EmailMessage()
    msg['Subject'] = 'FedNet - Please verify your email!'
    msg['From'] = current_app.config['EMAIL_ADDRESS']
    msg['To'] = send_to

    # Create the secret key based on our little secret :)
    secret = URLSafeTimedSerializer(current_app.config['EMAIL_SECRET'])

    # Create token based on a user their email and salt to prevent same token.
    token = secret.dumps(send_to,
                         salt=current_app.config['EMAIL_REGISTER_SALT'])

    # Create link with token and add it to the body of the mail.
    link = url_for('data_mail.confirm_email', token=token, _external=True)

    # Load the HTML template for the email, and embed the information needed.
    with open('app/templates/email_template/verify-mail.html') as f:
        html = f.read()
    html = html.replace('VERIFY_LINK_HERE', link)
    html = html.replace('USERNAME_HERE', user[0] + ' ' + user[1])
    msg.add_alternative(html, subtype='html')

    # Add image to the contents of the email
    with open('app/static/images/LogoBackOpaque.png', 'rb') as img:
        # Know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # Attach it to the email. The cid='0' is linked to the cid in the html,
        # which loads it.
        msg.get_payload()[0].add_related(img.read(), maintype=maintype,
                                         subtype=subtype, cid='0')

    # Connect to the mailserver from google and send the e-mail.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(current_app.config['EMAIL_ADDRESS'],
                   current_app.config['EMAIL_PASSWORD'])
        smtp.send_message(msg)

    return good_json_response('success')


@blueprint.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        # Create the secret key based on our little secret :)
        secret = URLSafeTimedSerializer(current_app.config['EMAIL_SECRET'])

        # Confirm key is in pool and has not expired yet.
        email = secret.loads(token, max_age=3600,
                             salt=current_app.config['EMAIL_REGISTER_SALT'])

        # If user exists update the status 'email_confirmed' to 1.
        # The user will now be able to login.
        if users.exists(email=email):
            users.update({'email_confirmed': 1}, email=email)

            # Redirect the user to the login page, trigger
            # 'registration complete' process.
            return redirect(
                get_central_ip() +
                '?message=registration_complete')
        else:
            return bad_json_response('No user with the email ' + email
                                     + ' exists.')
    except SignatureExpired:
        message = 'The token has expired, please try registering again.'
        return redirect(get_central_ip() + '?message=' + message)

    except BadTimeSignature:
        message = 'The token did not match. Are you trying to hack FedNet? Q_Q'
        return redirect(get_central_ip() + '?message=' + message)


@blueprint.route('/forgotpass', methods=['POST'])
def forgotpass():
    # Check if
    username = request.form['username']

    if not username:
        return bad_json_response("Bad request: Missing parameter 'username'.")

    # Retrieve email for given username.
    # Also retrieve firstname and lastname for personal message.
    firstname, lastname, send_to = users.export_one('firstname', 'lastname',
                                                    'email', username=username)

    # If no user is found give an error.
    if not firstname or not lastname or not username:
        return bad_json_response('Error retrieving the user.')

    # stuur mail met new ww link
    # Construct message object with receipient and sender
    msg = EmailMessage()
    msg['Subject'] = 'FedNet - Change your password.'
    msg['From'] = current_app.config['EMAIL_ADDRESS']
    msg['To'] = send_to

    # Create the secret key based on our little secret :)
    secret = URLSafeTimedSerializer(current_app.config['EMAIL_SECRET'])

    # Create token based on a user their email and salt to prevent same token.
    token = secret.dumps(send_to,
                         salt=current_app.config['EMAIL_FORGOTPASS_SALT'])

    # Create link with token and username so central knows how to handle it.
    parameters = '?username=' + username + '&token=' + token
    link = get_central_ip() + '/forgotPassword' + parameters

    # Load the HTML template for the email, and embed the information needed.
    with open('app/templates/email_template/forgot-password.html') as f:
        html = f.read()
    html = html.replace('LINK_HERE', link)
    html = html.replace('USERNAME_HERE', username)
    html = html.replace('NAME_HERE', firstname + ' ' + lastname)
    msg.add_alternative(html, subtype='html')

    # Add image to the contents of the email
    with open('app/static/images/LogoBackOpaque.png', 'rb') as img:
        # Know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # Attach it to the email. The cid='0' is linked to the cid in the html,
        # which loads it.
        msg.get_payload()[0].add_related(img.read(), maintype=maintype,
                                         subtype=subtype, cid='0')

    # Connect to the mailserver from google and send the e-mail.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(current_app.config['EMAIL_ADDRESS'],
                   current_app.config['EMAIL_PASSWORD'])
        smtp.send_message(msg)

    return good_json_response('success')


@blueprint.route('/confirm_forgotpass', methods=['POST'])
def confirm_forgotpass():
    try:
        token = request.form['token']
        password = request.form['password']

        # Create the secret key based on our little secret :)
        secret = URLSafeTimedSerializer(current_app.config['EMAIL_SECRET'])

        # Confirm key is in pool and has not expired yet.
        # Extract email from secret.
        email = secret.loads(token, max_age=3600,
                             salt=current_app.config['EMAIL_FORGOTPASS_SALT'])

        # Error if no user with given email is found.
        if not users.exists(email=email):
            return bad_json_response('No user with the email ' + email
                                     + ' exists.')

        # Encrypt password for storage in database.
        password = sha256_crypt.encrypt(request.form['password'])
        users.update({'password': password}, email=email)

        return good_json_response('Change password succesfull')
    except SignatureExpired:
        message = 'The token has expired, please try requesting a new password.'
        return redirect(get_central_ip() + '?message=' + message)
    except BadTimeSignature:
        message = (
            'The token did not match. Are you trying to hack some user? Q_Q'
        )
        return redirect(get_central_ip() + '?message=' + message)


@blueprint.route('/forgot_username', methods=['POST'])
def forgot_username():
    email = request.form['email']

    if not email:
        return bad_json_response("Bad request: Missing parameter 'email'.")

    # Retrieve email for given username.
    # Also retrieve firstname and lastname for personal message.
    username = users.export_one('username', email=email)

    # If no user is found for given email, don't send email.
    if not username:
        return bad_json_response(
            'No user with this e-mail exists on this server: ' + get_own_ip()
        )

    # Construct message object with receipient and sender
    msg = EmailMessage()
    msg['Subject'] = 'FedNet - Your username is ' + username
    msg['From'] = current_app.config['EMAIL_ADDRESS']
    msg['To'] = email

    # Load the HTML template for the email, and embed the information needed.
    with open('app/templates/email_template/forgot-username.html') as f:
        html = f.read()
    html = html.replace('USERNAME_HERE', username)
    msg.add_alternative(html, subtype='html')

    # Add image to the contents of the email
    with open('app/static/images/LogoBackOpaque.png', 'rb') as img:
        # Know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # Attach it to the email. The cid='0' is linked to the cid in the html,
        # which loads it.
        msg.get_payload()[0].add_related(img.read(), maintype=maintype,
                                         subtype=subtype, cid='0')
    # Connect to the mailserver from google and send the e-mail.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(current_app.config['EMAIL_ADDRESS'],
                   current_app.config['EMAIL_PASSWORD'])
        smtp.send_message(msg)

    return good_json_response(('Email was sent to ' + email + '.'))


__all__ = ('blueprint',)
