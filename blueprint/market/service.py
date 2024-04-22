from blueprint.market.exchange import binance, coinbase
import pandas as pd


class Funding:
    def __init__(self):
        self.df = pd.concat([
            binance.get_funding(),
            coinbase.get_funding()
        ], ignore_index=True)

    def query(self, markPrice=None, indexPrice=None, fundingRate=None, interestRate=None, nextFundingTime=(),
              exchange=None):
        data = self.df.copy()
        data['markPrice'] = data['markPrice'].astype(float).round(2)
        data['indexPrice'] = data['indexPrice'].astype(float).round(2)
        data['fundingRate'] = data['fundingRate'].astype(float)
        data['interestRate'] = data['interestRate'].astype(float)

        if markPrice:
            data = self.filter_numeric_column(data, 'marlPrice', markPrice)
        if indexPrice:
            data = self.filter_numeric_column(data, 'indexPrice', indexPrice)
        if fundingRate:
            data = self.filter_numeric_column(data, 'fundingRate', fundingRate)
        if interestRate:
            data = self.filter_numeric_column(data, 'interestRate', interestRate)
        if nextFundingTime:
            data = data[data['nextFundingTime'].isin(nextFundingTime)]
        if exchange and exchange != 'all':
            data = data[data['exchange'] == exchange]

        payload = {
            'exchange': list(self.df['exchange'].value_counts().keys()),
            'nextFundingTime': list(self.df['nextFundingTime'].dt.strftime('%Y-%m-%d %H:%M:%S').value_counts().keys()),
            'data': data.sort_values('nextFundingTime').reset_index(drop=True).to_dict(orient='index')
        }
        return payload

    def filter_numeric_column(self, df, column, rule=1):

        if rule == '1':
            return df
        elif rule == '2':
            return df[
                (df[column] > df[column].mean() + df[column].std()) &
                (df[column] < df[column].mean() + 2 * df[column].std())
                ]
        elif rule == '3':
            return df[
                (df[column] > df[column].mean()) &
                (df[column] < df[column].mean() + df[column].std())
                ]
        elif rule == '4':
            return df[
                (df[column] < df[column].mean()) &
                (df[column] > df[column].mean() - df[column].std())
                ]
        elif rule == '5':
            return df[
                (df[column] < df[column].mean() + df[column].std()) &
                (df[column] > df[column].mean() - 2 * df[column].std())
                ]
        else:
            return df
