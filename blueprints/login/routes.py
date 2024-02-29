from flask import Blueprint
from flask import request, send_file, render_template, url_for, session

from package.response import Response
from package.database_model import *
from package.database_operator import *

login_blueprints = Blueprint('login', __name__, template_folder='templates')


@login_blueprints.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@login_blueprints.route('/api', methods=['POST'])
def login_api():
    payload = {
        'email_address': request.form['email_address'],
        'password': request.form['password'],
    }

    user = DatabaseOperator.select_one(User, payload)
    if user is None:
        return Response.client_error('User not found', 'either email address or password is incorrect')

    session['email_address'] = request.form['email_address']
    session['id'] = user.id

    return Response.response('response', 'User logged in successfully')
