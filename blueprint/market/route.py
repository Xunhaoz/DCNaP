import pandas as pd
from flask import Blueprint, render_template, request, jsonify
from models.database import db, User, GoodUser
import blueprint.market.service as service
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    goods_user = service.Funding().get_good_user(get_jwt_identity()["id"])
    return render_template("/invoice.html", goods_user=goods_user, user=get_jwt_identity())


@market.route("/add_goods", methods=["POST"])
@jwt_required()
def add_goods():
    payload = request.json
    good_user = GoodUser(
        user_id=get_jwt_identity()["id"],
        symbol=payload['symbol'],
        funding_rate=payload['funding_rate'],
        mark_price=payload['mark_price'],
        index_price=payload['index_price'],
        interest_rate=payload['interest_rate'],
        direction=payload['direction']
    )
    db.session.add(good_user)
    db.session.commit()
    return jsonify({"message": "add goods successfully"})


@market.route("/top-up")
@jwt_required()
def top_up():
    goods_user = service.Funding().get_good_user(get_jwt_identity()["id"])
    return render_template("/pricing.html", goods_user=goods_user, user=get_jwt_identity())
