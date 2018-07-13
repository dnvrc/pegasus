import pandas as pd
import sqlite3 as sq3

from src.config import Config


if __name__ == '__main__':
    config = Config()
    sqlite = sq3.connect('/Users/alexmanelis/Development/Python/cryptocurrency-analysis/database.db')

    frame = {}
    coins = [
        {'slug': 'bitcoin', 'symbol': 'btc', 'data': None},
        {'slug': 'ethereum', 'symbol': 'eth', 'data': None},
        {'slug': 'litecoin', 'symbol': 'ltc', 'data': None},
        {'slug': 'monero', 'symbol': 'xmr', 'data': None},

        {'slug': 'bitcoin-diamond', 'symbol': 'bcd', 'data': None},
        {'slug': 'bitcoin-gold', 'symbol': 'bcg', 'data': None},
        {'slug': 'dash', 'symbol': 'dash', 'data': None},
        {'slug': 'marijuanacoin', 'symbol': 'mar', 'data': None},
        {'slug': 'zcash', 'symbol': 'zec', 'data': None},
    ]

    for indx, coin in enumerate(coins):
        slug = coin.get('slug', None)

        if slug is None:
            continue

        rest = pd.read_sql_query(f'SELECT * FROM val WHERE currency_slug = "{slug}" ORDER BY "datetime" DESC limit 10000;', sqlite)

        coins[indx]['data'] = rest
        frame[slug] = rest['price_usd']

    print(pd.DataFrame(frame).corr())
