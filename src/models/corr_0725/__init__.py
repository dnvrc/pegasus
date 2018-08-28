import sqlite3 as sq3

from src.config import Config
from src.models import Model
from src.models.corr_0725.pipeline import Pipeline
from src.models.corr_0725.reader import Reader


if __name__ == '__main__':
    config = Config()
    sqlite = sq3.connect('/Users/alexmanelis/Development/Python/coinmarketcap-scraper/database.db')

    # Define a schema for the process function
    model = Model(period=[2018,2017,2016], entities=[
        {'slug': 'bitcoin',             'symbol': 'btc',  'algo': 'sha-256'},
        {'slug': 'bitcoin-cash',        'symbol': 'bch',  'algo': 'sha-256'},
        {'slug': 'bitcoin-diamond',     'symbol': 'bcd',  'algo': 'X13'},
        {'slug': 'bitcoin-gold',        'symbol': 'bcg',  'algo': 'equihash'},
        {'slug': 'bitcoin-private',     'symbol': 'btcp', 'algo': 'equihash'},
        {'slug': 'dash',                'symbol': 'dash', 'algo': 'X11'},
        {'slug': 'electroneum',         'symbol': 'etn',  'algo': 'cryptonight'},
        {'slug': 'ethereum',            'symbol': 'eth',  'algo': 'ethash'},
        {'slug': 'ethereum-classic',    'symbol': 'etc',  'algo': 'ethash'},
        {'slug': 'litecoin',            'symbol': 'ltc',  'algo': 'scrypt'},
        {'slug': 'galactrum',           'symbol': 'ore',  'algo': 'lyra2rev2'},
        {'slug': 'monero',              'symbol': 'xmr',  'algo': 'cryptonight'},
        {'slug': 'ravencoin',           'symbol': 'rvn',  'algo': 'X16R'},
        {'slug': 'zcash',               'symbol': 'zec',  'algo': 'equihash'},
    ])

    # Pipeline(config, sqlite, model).process()
    Reader(config, sqlite, model).process()
