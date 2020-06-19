import os
import smtplib
import imghdr
from email.message import EmailMessage
from flask import Blueprint, request
from email.mime.text import MIMEText

# EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
blueprint = Blueprint('data_mail', __name__)

@blueprint.route('/', strict_slashes=False)
def test():
    return "test"

@blueprint.route('/verification', strict_slashes=False)
def send_verification_mail():
    EMAIL_ADDRESS = "therealfednet@gmail.com"
    EMAIL_PASSWORD = "fednetbest1"

    msg = EmailMessage()
    msg['Subject'] = 'FedNet - Please verify your email!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'michelrummens@hotmail.com'

    # html = open("app/api/data/simple.html")
    # msg2 = MIMEText(html.read(), 'html')

    # msg.set_content(msg2)

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">This is an HTML Email!</h1>
        </body>
    </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)