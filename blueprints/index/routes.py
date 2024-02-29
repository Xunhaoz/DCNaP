from flask import Blueprint
from flask import request, send_file, render_template, url_for, session

from package.response import Response
from package.database_model import *
from package.database_operator import *

index_blueprints = Blueprint('index', __name__, template_folder='templates')


@index_blueprints.route('/', methods=['GET'])
def index():
    user = DatabaseOperator.select_one(User, {'id': session['id']})
    return render_template('index.html', user=user)
