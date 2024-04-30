from models.database import db, User, GoodUser
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

        if exchange and exchange != 'all':
            data = data[data['exchange'] == exchange]
        if nextFundingTime:
            data = data[data['nextFundingTime'].isin(nextFundingTime)]
        if markPrice:
            data = self.filter_numeric_column(data, 'markPrice', markPrice)
        if indexPrice:
            data = self.filter_numeric_column(data, 'indexPrice', indexPrice)
        if fundingRate:
            data = self.filter_numeric_column(data, 'fundingRate', fundingRate)
        if interestRate:
            data = self.filter_numeric_column(data, 'interestRate', interestRate)

        payload = {
            'exchange': list(self.df['exchange'].value_counts().keys()),
            'nextFundingTime': list(self.df['nextFundingTime'].dt.strftime('%Y-%m-%d %H:%M:%S').value_counts().keys()),
            'data': data.sort_values('nextFundingTime').reset_index(drop=True).to_dict(orient='index')
        }
        return payload

    def filter_numeric_column(self, df, column, rule=1):
        mean = df[column].mean()
        std = df[column].std() + 1e-6

        if rule == '1':
            return df
        elif rule == '2':
            return df[
                (df[column] >= mean + std) &
                (df[column] < mean + 2 * std)
                ]
        elif rule == '3':
            return df[
                (df[column] >= mean) &
                (df[column] < mean + std)
                ]
        elif rule == '4':
            return df[
                (df[column] < mean) &
                (df[column] >= mean - std)
                ]
        elif rule == '5':
            return df[
                (df[column] < mean - std) &
                (df[column] >= mean - 2 * std)
                ]
        else:
            return df

    def row_processor(self, row):
        yield_ = None
        funding_rate, interest_rate, mark_price, index_price = \
            float(row['funding_rate']), float(row['interest_rate']), float(row['mark_price']), float(row['index_price'])
        if row['direction'] == '-1':
            yield_ = mark_price - index_price - index_price * funding_rate - interest_rate * index_price
        elif row['direction'] == '1':
            yield_ = index_price - mark_price - mark_price * funding_rate - interest_rate * mark_price
        return yield_

    def get_good_user(self, user_id):
        goods_user = GoodUser.query.filter_by(user_id=user_id).all()
        payload = [good_user.as_dict() for good_user in goods_user]
        df = pd.DataFrame(payload).set_index('id')
        df['net sale'] = df.apply(lambda x: self.row_processor(x), axis=1)
        df.sort_index(inplace=True)
        grouped_df = df.groupby('symbol').agg({
            'funding_rate': 'first',
            'mark_price': 'first',
            'index_price': 'first',
            'interest_rate': 'first',
            'direction': 'first',
            'net sale': 'sum',
            'symbol': 'count'
        }).rename(columns={'symbol': 'quantity'})
        grouped_df['direction'] = grouped_df['direction'].apply(lambda x: 'Long' if x == '1' else 'Short')
        grouped_df.reset_index(inplace=True)
        grouped_df['date'] = grouped_df['symbol'].apply(lambda x: ''.join(x.split()[1:]))
        grouped_df['symbol'] = grouped_df['symbol'].apply(lambda x: x.split()[0])
        sub_total = grouped_df['net sale'].sum()
        vat_rate = '20%'
        vat = sub_total * 0.2
        total_due = sub_total + vat
        payload = {
            'sub_total': sub_total,
            'vat_rate': vat_rate,
            'vat_due': vat,
            'total_due': total_due,
            'goods_user': grouped_df.to_dict(orient='index')
        }
        return payload
