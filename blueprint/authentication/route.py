from models.database import User, db
from flask import Blueprint, render_template, request
import hashlib

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
