import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Blueprint
from flask import request, send_file, render_template, url_for

from package.response import Response
from package.database_model import *
from package.database_operator import *

forget_password_blueprints = Blueprint('forget_password', __name__, template_folder='templates')


@forget_password_blueprints.route('/', methods=['GET'])
def forget_password():
    return render_template('forgot-password.html')


@forget_password_blueprints.route('/reset_password', methods=['GET'])
def reset_password():
    return render_template('reset-password.html')


@forget_password_blueprints.route('/reset_password_api', methods=['POST'])
def reset_password_api():
    email_address = request.form['email_address']
    password = request.form['password']
    DatabaseOperator.update(User, {'email_address': email_address}, {'password': password})
    return Response.response('response', 'Reset password successfully')


@forget_password_blueprints.route('/send_mail_api', methods=['POST'])
def forget_password_send_mail_api():
    payload = {
        'email_address': request.form['email_address'],
    }

    user = DatabaseOperator.select_one(User, payload)
    if user is None:
        return Response.client_error('User not found', 'email address is incorrect')

    smtp_server = 'smtp.gmail.com'
    port = 587
    password = 'ovuggtrwbbpmjkrx'
    sender_email = 'leo20020529@gmail.com'
    receiver_email = user.email_address

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user.email_address
    message["Subject"] = "Password Reset Instructions"

    body = f"""Hello {user.first_name} {user.last_name},
Please click on the following link to reset your password:
    
http://{request.headers.get('Host')}/forget_password/reset_password?email_address={user.email_address}

If you did not request this change, please ignore this email.

Thank you,
YourWebsite Team
    """
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()  # Close the SMTP server

    return Response.response('response', 'Password reset email hae been send')
