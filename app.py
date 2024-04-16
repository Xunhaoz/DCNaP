# -*- coding: utf-8 -*-
import secrets
import string

from blueprints.login.routes import *
from blueprints.register.routes import *
from blueprints.forget_password.routes import *
from blueprints.index.routes import *

from package.response import Response

from flask import Flask

app = Flask(__name__)
app.secret_key = ''.join(secrets.choice(string.ascii_letters) for i in range(10))

# blueprint
app.register_blueprint(login_blueprints, url_prefix='/login')
app.register_blueprint(forget_password_blueprints, url_prefix='/forget_password')
app.register_blueprint(register_blueprints, url_prefix='/register')
app.register_blueprint(index_blueprints, url_prefix='/index')

# SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DepartmentComputerNetworkProgramming.db"
db.init_app(app)
with app.app_context():
    db.create_all()


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    return Response.sever_error("sever error", str(e))


@app.route("/", methods=['GET'])
def test_connection():
    return Response.response('connect success')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5001)
