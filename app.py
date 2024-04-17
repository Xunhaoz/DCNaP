# -*- coding: utf-8 -*-
from blueprint.authentication.route import authentication
from blueprint.market.route import market
from models.database import db

from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

# SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DepartmentComputerNetworkProgramming.db"
app.register_blueprint(authentication)
app.register_blueprint(market)
db.init_app(app)

with app.app_context():
    db.session.close()
    db.drop_all()
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("error-404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return render_template("error-500.html"), 500


# @app.errorhandler(Exception)
# def handle_exception(e: Exception):
#     return Response.sever_error("sever error", str(e))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
