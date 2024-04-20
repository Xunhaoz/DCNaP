from flask import Blueprint, render_template
from models.database import Exchange, db

import blueprint.market.service as service

market = Blueprint(
    "market",
    __name__,
    url_prefix="/market",
    template_folder="templates",
    static_folder="../../static"
)


@market.route("/")
def marketOverview():

    fundings = []

    # for exchange in service.getExchanges():

    exchange = "binance"
    funding = service.Funding()
    funding.addExchange(exchange)
    funding.addPairs()

    fundings.append(funding)

    return render_template(
        "/job-listing.html",
        fundings=fundings,
    )


# @market.route("/loadData/<exchange>", methods=["GET"])
# def loadService(exchange):
#     fundings = service.getFunding()
#
#
#     return fundings["exchange"]


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
