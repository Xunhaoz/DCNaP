import pandas as pd
from flask import Blueprint, render_template, request, jsonify
from models.database import Exchange, db
import blueprint.market.service as service
from flask_jwt_extended import jwt_required

market = Blueprint(
    "market",
    __name__,
    url_prefix="/market",
    template_folder="templates",
    static_folder="../../static"
)


@market.route("/", methods=["GET"])
@jwt_required()
def market_overview():
    funding = service.Funding().query()
    return render_template(
        "job-listing.html",
        funding=funding
    )


@market.route("/", methods=["POST"])
@jwt_required()
def market_overview_query():
    payload = dict(request.form.lists())

    exchange = payload["exchange"][0]
    next_funding_time = pd.to_datetime(payload["fundingTime"]).tz_localize('Asia/Taipei').tolist()
    markPrice = payload["form-market"][0]
    indexPrice = payload["form-index"][0]
    fundingRate = payload["form-funding"][0]
    interestRate = payload["form-interest"][0]

    funding = service.Funding().query(
        exchange=exchange, nextFundingTime=next_funding_time, markPrice=markPrice, indexPrice=indexPrice,
        fundingRate=fundingRate, interestRate=interestRate
    )
    return jsonify(funding)


@market.route("/invoice")
@jwt_required()
def invoice():
    return render_template("/invoice.html")
