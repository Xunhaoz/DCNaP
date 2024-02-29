import re

from flask import Blueprint
from flask import request, render_template

from package.response import Response
from package.database_operator import *

from script.utils import *

register_blueprints = Blueprint('register', __name__, template_folder='templates')


@register_blueprints.route('/', methods=['GET'])
def register():
    return render_template('register.html')


@register_blueprints.route('/api', methods=['POST'])
def register_api():
    payload = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email_address': request.form['email_address'],
        'password': request.form['password'],
    }

    for k, v in payload.items():
        if is_input_null(v):
            return Response.client_error('client error', f'{k} should not be empty')

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, payload['email_address']):
        return Response.client_error('client error', f'Formate of email address is not correct')

    if len(payload['password']) < 8:
        return Response.client_error('client error', 'Password length should be at least 8 characters')

    DatabaseOperator.insert(User, payload)
    return Response.response('response', 'register successfully')
