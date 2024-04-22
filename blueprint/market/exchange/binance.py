import pandas as pd


def get_funding():
    """
    https://www.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT
    [
        'symbol', 'markPrice', 'indexPrice', 'estimatedSettlePrice', 'lastFundingRate', 'interestRate',
        'nextFundingTime', 'time'
    ]
    """
    url = "https://www.binance.com/fapi/v1/premiumIndex"
    df = pd.read_json(url)
    timezone_convertor = lambda x: x.tz_convert('Asia/Taipei')
    df['nextFundingTime'] = pd.to_datetime(df['nextFundingTime'], unit='ms', utc=True).map(timezone_convertor)
    df['time'] = pd.to_datetime(df['time'], unit='ms', utc=True).map(timezone_convertor)
    df['exchange'] = 'Binance'
    df.columns = [
        'symbol', 'markPrice', 'indexPrice', 'estimatedSettlePrice', 'fundingRate', 'interestRate',
        'nextFundingTime', 'time', 'exchange'
    ]

    return df[['symbol', 'markPrice', 'indexPrice', 'fundingRate', 'interestRate', 'nextFundingTime', 'exchange']]
