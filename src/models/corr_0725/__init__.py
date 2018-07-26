import sqlite3 as sq3

from src.config import Config
from src.models import Model
from src.models.corr_0725.pipeline import Pipeline


if __name__ == '__main__':
    config = Config()
    sqlite = sq3.connect('/Users/alexmanelis/Development/Python/coinmarketcap-scraper/database.db')

    # Define a schema for the process function
    model = Model(period=[2018, 2017, 2016, 2015, 2014, 2013], entities=[
        {'slug': 'bitcoin', 'symbol': 'btc'},
        {'slug': 'ethereum', 'symbol': 'eth'},
        {'slug': 'litecoin', 'symbol': 'ltc'},
        {'slug': 'monero', 'symbol': 'xmr'},

        {'slug': 'bitcoin-diamond', 'symbol': 'bcd'},
        {'slug': 'bitcoin-gold', 'symbol': 'bcg'},
        {'slug': 'dash', 'symbol': 'dash'},
        {'slug': 'marijuanacoin', 'symbol': 'mar'},
        {'slug': 'zcash', 'symbol': 'zec'},
    ])

    Pipeline(config, sqlite, model).process()
