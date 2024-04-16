from flask import Blueprint, render_template

authentication = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
    template_folder="templates",
    static_folder="static"
)


@authentication.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")


@authentication.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")


@authentication.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")
