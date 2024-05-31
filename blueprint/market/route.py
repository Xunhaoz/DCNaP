import pandas as pd
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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
    if not User.query.filter_by(id=get_jwt_identity()["id"]).first():
        return redirect(url_for('authentication.sign_in'))

    funding = service.Funding().query()
    return render_template(
        "job-listing.html",
        funding=funding
    )


@market.route("/", methods=["POST"])
@jwt_required()
def market_overview_query():
    if not User.query.filter_by(id=get_jwt_identity()["id"]).first():
        return redirect(url_for('authentication.sign_in'))

    print(request.form)
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
    if not User.query.filter_by(id=get_jwt_identity()["id"]).first():
        return redirect(url_for('authentication.sign_in'))

    goods_user = service.Funding().get_good_user(get_jwt_identity()["id"])
    return render_template("/invoice.html", goods_user=goods_user, user=get_jwt_identity())


@market.route("/add_goods", methods=["POST"])
@jwt_required()
def add_goods():
    if not User.query.filter_by(id=get_jwt_identity()["id"]).first():
        return redirect(url_for('authentication.sign_in'))

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


@market.route("/deposit", methods=["POST"])
@jwt_required()
def deposit_money():
    if not User.query.filter_by(id=get_jwt_identity()["id"]).first():
        return redirect(url_for('authentication.sign_in'))

    payload = request.json
    user = User.query.filter_by(id=get_jwt_identity()["id"]).first()
    service.PriceCard().update_price_card(f'PriceCard{payload["amount"]}')
    user.deposit = user.deposit + float(payload["amount"])
    db.session.commit()
    return jsonify({"message": "add deposit successfully"})


@market.route("/top-up")
@jwt_required()
def top_up():
    if not User.query.filter_by(id=get_jwt_identity()["id"]).first():
        return redirect(url_for('authentication.sign_in'))

    goods_user = service.Funding().get_good_user(get_jwt_identity()["id"])
    price_card = service.PriceCard().get_price_card()
    return render_template("/pricing.html", goods_user=goods_user, user=get_jwt_identity(), price_card=price_card)
