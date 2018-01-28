import pickle
import quandl

import pandas as pd

from src.api.base import APIBase


class Generic(APIBase):
    @classmethod
    def get_json_data(self, json_url, cache_path):
        cache_path = f'{cache_path}.pkl'.replace('/','-')
        cache_path = f'./tmp/{cache_path}'

        try:
            f = open(cache_path, 'rb')
            df = pickle.load(f)
        except (OSError, IOError) as e:
            df = pd.read_json(json_url)
            df.to_pickle(cache_path)

        return df
