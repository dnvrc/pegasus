from datetime import datetime

from src.api.base import APIBase
from src.api.generic import Generic


class PoloniexAPI(APIBase):
    def get_exchange_data(self, btc_usd_datasets, btc_usd_avg_col, altcoins=['ETH','ETC','LTC','XRP','STR','DASH','SC','XMR','XEM']):
        altcoin_data = {}

        for altcoin in altcoins:
            altcoin_data[altcoin] = self.get_crypto_data(f'BTC_{altcoin}')
            altcoin_data[altcoin]['price_usd'] =  altcoin_data[altcoin]['weightedAverage'] * btc_usd_datasets[btc_usd_avg_col]

        return altcoin_data

    def get_crypto_data(self, pair):
        s_date = datetime.strptime('2015-01-01', '%Y-%m-%d')
        e_date = datetime.now()

        base_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
        json_url = base_url.format(pair, s_date.timestamp(), e_date.timestamp(), 86400)

        data_df = Generic.get_json_data(json_url, pair)
        data_df = data_df.set_index('date')

        return data_df
