from flask import Blueprint, render_template
from models.database import Exchange, db

import blueprint.market.service

market = Blueprint(
    "market",
    __name__,
    url_prefix="/market",
    template_folder="templates",
    static_folder="../../static"
)


@market.route("/")
def marketOverview():
    return render_template("/job-listing.html")


@market.route("/loadData", methods=["GET"])
def loadService():
    print("herererererer")
    print(Exchange.query.all())

    exchanges = Exchange.query.all()

    for e in exchanges:

    print("herererererer")

    return render_template("/layout-navbar-overlap.html")



@market.route("/dashboard")
def dashboard():
    return render_template("/layout-navbar-overlap.html")



# @market.route("/add", methods=["GET"])
# def temp():
#     temp = Exchange(name="Binance")
#     temp2 = Exchange(name="Coinbase")
#
#     db.session.add(temp)
#     db.session.add(temp2)
#
#     db.session.commit()
#
#     return {"message": "User created successfully"}, 200
