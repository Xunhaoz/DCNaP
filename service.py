import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


class IndexService:
    def __init__(self):
        benchmark = self.get_currencies_rank()
        self.payload = {
            'all_crypto_currency': self.get_all_crypto_currency(),
            'popular_currencies': benchmark[0],
            'new_coins_listed': benchmark[1],
            'largest_increase': benchmark[2],
            'highest_trading_volume': benchmark[3],
            'history': self.get_currency_history()
        }

    def get_index(self):
        return self.payload

    def filter_currency_image(self, image_urls):
        img_need_download = []
        img_downloaded = [p.name for p in Path('./static/img/coin').glob('*')]
        local_img = [f'./static/img/coin/{img_url.split("/")[-1]}' for img_url in image_urls]
        for img_url in image_urls:
            if img_url.split('/')[-1] not in img_downloaded:
                img_need_download.append(img_url)
        return img_need_download, local_img

    def get_currencies_rank(self):
        resp = requests.get('https://www.binance.com/zh-TC/markets/overview')
        soup = BeautifulSoup(resp.text, 'html.parser')
        elements = soup.findAll(class_='w-full css-vurnku')
        currencies_rank = []
        list_of_img_need_downloads = []
        for element in elements:
            srcs = [e.get('src') for e in element.findAll('img')]
            symbol = [e.text for e in element.findAll(class_='css-10dum4v')]
            price = [e.text for e in element.findAll(style='direction:ltr')]
            pct_change = [p for k, p in enumerate(price) if k % 2 == 1]
            price = [p for k, p in enumerate(price) if k % 2 == 0]
            img_need_downloads, local_imgs = self.filter_currency_image(srcs)
            list_of_img_need_downloads.extend(img_need_downloads)

            currencies_rank.append(pd.DataFrame({
                'src': local_imgs,
                'symbol': symbol,
                'price': price,
                'pct_change': pct_change,
            }).to_dict(orient='records'))

        with ThreadPoolExecutor() as executor:
            executor.map(self.cache_image, list_of_img_need_downloads)
        return currencies_rank

    def get_all_crypto_currency(self):
        resp = requests.get('https://www.binance.com/zh-TC/markets/overview')
        soup = BeautifulSoup(resp.text, 'html.parser')
        elements = soup.find(class_='css-1pysja1').findAll(class_='css-1ydqfmf')

        element_data_list = []
        srcs = []
        for element in elements:
            element_data = element.get_text(strip=True, separator='|').split('|')
            element_data.append(element.find(class_='rounded-full').get('src'))
            srcs.append(element_data[-1])
            element_data[-1] = f"./static/img/coin/{element_data[-1].split('/')[-1]}"
            element_data_list.append(element_data)

        img_need_downloads, local_imgs = self.filter_currency_image(srcs)

        with ThreadPoolExecutor() as executor:
            executor.map(self.cache_image, img_need_downloads)

        df = pd.DataFrame(element_data_list)
        df.columns = ['symbol_1', 'symbol_2', 'price', 'change', 'volume', 'market_price', 'image']
        return df.to_dict(orient='records')

    def get_currency_history(self):
        day = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        spot_request_payload = {
            "bizType": "SPOT", "productName": "klines", "symbolRequestItems": [
                {
                    "endDay": day,
                    "granularityList": ["1m"],
                    "interval": "daily",
                    "startDay": day,
                    "symbol": "ETHUSDT"
                }
            ]
        }

        future_request_payload = {
            "bizType": "FUTURES_UM", "productName": "klines", "symbolRequestItems": [
                {
                    "endDay": day,
                    "granularityList": ["1m"],
                    "interval": "daily",
                    "startDay": day,
                    "symbol": "ETHUSDT"
                }
            ]
        }

        def get_history_data(payload):
            download_item = requests.post(
                "https://www.binance.com/bapi/bigdata/v1/public/bigdata/finance/exchange/listDownloadData2",
                json=payload
            ).json()['data']['downloadItemList'][0]
            filename, url = download_item['filename'], download_item['url']

            header = 0
            if payload['bizType'] == 'SPOT':
                filename = 'SPOT_' + filename
                header = None

            self.download_history(filename, url)
            data = pd.read_csv(
                f'./static/history/{filename}', header=header, names=[
                    "open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count",
                    "taker_buy_volume", "taker_buy_quote_volume", "ignore"
                ])

            now = datetime.now()
            minutes_of_day = now.hour * 60 + now.minute

            return filename, \
                data['close'].tolist()[minutes_of_day - 60:minutes_of_day], \
                data['open_time'].apply(
                    lambda ts: datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
                ).tolist()[minutes_of_day - 60:minutes_of_day]

        spot_filename, spot_data, ts = get_history_data(spot_request_payload)
        future_filename, future_data, ts = get_history_data(future_request_payload)

        payload = {
            'spot': spot_data,
            'future': future_data,
            'datetime': ts
        }
        return payload

    def cache_image(self, img_url):
        pic = requests.get(img_url)
        with open(f"./static/img/coin/{img_url.split('/')[-1]}", 'wb') as f:
            f.write(pic.content)

    def download_history(self, filename, url):
        resp = requests.get(url)
        with open(f"./static/history/{filename}", 'wb') as f:
            f.write(resp.content)
