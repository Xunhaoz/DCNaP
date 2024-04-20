import hashlib
import uuid

from models.database import User, db
from models.email import mail
from flask_mail import Message
from flask import Blueprint, render_template, request, make_response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token, \
    set_access_cookies, set_refresh_cookies, unset_access_cookies, unset_refresh_cookies
from itsdangerous import URLSafeSerializer

authentication = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
    template_folder="templates",
    static_folder="../../static"
)


@authentication.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")


@authentication.route("/sign-up", methods=["GET"])
def sign_up():
    return render_template("sign-up.html")


@authentication.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")


@authentication.route("/terms-of-service")
def terms_of_service():
    return render_template("terms-of-service.html")


@authentication.route("/sign-up", methods=["POST"])
def create_user():
    try:
        if User.query.filter_by(email=request.form["email"]).first():
            return {"message": "User already exists"}, 400

        password = hashlib.md5(request.form["password"].encode()).hexdigest()
        user = User(name=request.form["name"], email=request.form["email"], password=password)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 200

    except Exception as e:
        return {"message": "Some error happened"}, 500


@authentication.route("/sign-in", methods=["POST"])
def sign_in_user():
    password = hashlib.md5(request.form["password"].encode()).hexdigest()
    user = User.query.filter_by(email=request.form["email"], password=password).first()
    if user is None:
        return {"message": "Invalid credentials"}, 400

    access_token = create_access_token(identity=user.as_dict())
    refresh_token = create_refresh_token(identity=user.as_dict())
    response = make_response(jsonify({"message": "User logged in successfully"}), 200)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@authentication.route("/sign-out", methods=["POST"])
@jwt_required()
def sign_out_user():
    response = make_response(jsonify({"message": "User logged out successfully"}), 200)
    unset_access_cookies(response)
    unset_refresh_cookies(response)
    return response


@authentication.route("/forgot-password", methods=["POST"])
def send_password_user():
    user = User.query.filter_by(email=request.form["email"]).first()
    if user is None:
        return {"message": "User not found"}, 400

    try:
        mail_message = Message(
            'Password reset request',
            sender='leo20020529@gmail.com',
            recipients=[request.form["email"]]
        )
        s = URLSafeSerializer('password-reset')
        mail_message.html = render_template(
            "email.html",
            token=s.dumps(user.email)
        )
        mail.send(mail_message)
    except Exception as e:
        print(e)
        return {"message": "Some error happened"}, 500

    return {"message": "Email has sent, please check your email to update password"}, 200


@authentication.route("/update-password/<token>")
def update_password(token):
    return render_template('update-password.html', token=token)


@authentication.route("/update-password/<token>", methods=["PATCH"])
def update_user_password(token):
    s = URLSafeSerializer('password-reset')
    email = s.loads(token)
    User.query.filter_by(email=email).update({"password": hashlib.md5(request.form["password"].encode()).hexdigest()})
    db.session.commit()
    return {"message": "Password updated successfully"}
