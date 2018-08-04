import sqlite3 as sq3

from src.config import Config
from src.models import Model
from src.models.corr_0725.pipeline import Pipeline


if __name__ == '__main__':
    config = Config()
    sqlite = sq3.connect('/Users/alexmanelis/Development/Python/coinmarketcap-scraper/database.db')

    # Define a schema for the process function
    model = Model(period=[2018, 2017, 2016, 2015, 2014, 2013], entities=[
        {'slug': 'bitcoin',         'symbol': 'btc',  'algo': 'sha-256'},
        {'slug': 'ethereum',        'symbol': 'eth',  'algo': 'dagger-hashimoto'},
        {'slug': 'litecoin',        'symbol': 'ltc',  'algo': 'scrypt'},
        {'slug': 'monero',          'symbol': 'xmr',  'algo': 'cryptonight'},

        {'slug': 'bitcoin-diamond', 'symbol': 'bcd',  'algo': 'X13'},
        {'slug': 'dash',            'symbol': 'dash', 'algo': 'X11'},
        {'slug': 'marijuanacoin',   'symbol': 'mar',  'algo': 'X11'},
        {'slug': 'bitcoin-gold',    'symbol': 'bcg',  'algo': 'equihash'},
        {'slug': 'bitcoin-private', 'symbol': 'BTCP', 'algo': 'equihash'},
        {'slug': 'zcash',           'symbol': 'zec',  'algo': 'equihash'},
    ])

    Pipeline(config, sqlite, model).process()
