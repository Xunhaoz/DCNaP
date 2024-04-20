# -*- coding: utf-8 -*-
from blueprint.authentication.route import authentication
from models.database import db
from config import Config
from flask import Flask, render_template
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, set_access_cookies, get_jwt_identity
from datetime import datetime, timedelta, timezone
from models.email import mail

app = Flask(__name__, template_folder="templates", static_folder="static")

# SQLALCHEMY
app.config.from_object(Config)
app.register_blueprint(authentication)
db.init_app(app)
JWTManager(app)
mail.init_app(app)

with app.app_context():
    # db.session.close()
    # db.drop_all()
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("error-404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return render_template("error-500.html"), 500


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5001)
