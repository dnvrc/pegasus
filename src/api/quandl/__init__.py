import pickle
import quandl

import pandas as pd

from src.api.base import APIBase


class QuandlAPI(APIBase):    
    def get_exchange_data(self, exchanges=['COINBASE','BITSTAMP','ITBIT', 'KRAKEN']):
        exchange_data = {}

        for exchange in exchanges:
            exchange_data[exchange] = self.get_quandl_data(f'BCHARTS/{exchange}USD')

        return exchange_data

    def get_quandl_data(self, quandl_id):
        cache_path = f'{quandl_id}.pkl'.replace('/','-')
        cache_path = f'./tmp/{cache_path}'

        try:
            f = open(cache_path, 'rb')
            df = pickle.load(f)
        except (OSError, IOError) as e:
            df = quandl.get(quandl_id, returns='pandas')
            df.to_pickle(cache_path)

        return df
