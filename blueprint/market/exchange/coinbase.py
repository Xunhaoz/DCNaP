import pandas as pd
import requests


def get_funding():
    """
    https://www.coinbase.com/unauthed/api/v3/brokerage/products?product_type=FUTURE&contract_expiry_type=PERPETUAL&product_venue=FCM
    """
    url = "https://www.coinbase.com/unauthed/api/v3/brokerage/products?product_type=FUTURE&contract_expiry_type=PERPETUAL"

    response = requests.get(url).json()
    products = pd.DataFrame(response["products"])

    symbol = products['display_name'].apply(lambda x: x.split()[0]) + products['quote_name']
    markPrice = products['mid_market_price']
    indexPrice = products['price']

    perpetual_details = pd.DataFrame(
        pd.DataFrame(products['future_product_details'].tolist())['perpetual_details'].tolist()
    )
    interestRate = perpetual_details['open_interest']
    fundingRate = perpetual_details['funding_rate']
    timezone_convertor = lambda x: x.floor('s').tz_convert('Asia/Taipei')
    nextFundingTime = pd.to_datetime(perpetual_details['funding_time'], format='ISO8601', utc=True) \
        .map(timezone_convertor)

    return pd.DataFrame({
        'symbol': symbol,
        'markPrice': markPrice,
        'indexPrice': indexPrice,
        'fundingRate': fundingRate,
        'interestRate': interestRate,
        'nextFundingTime': nextFundingTime,
        'exchange': 'Coinbase'
    })

