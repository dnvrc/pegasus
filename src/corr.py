import pandas as pd
import sqlite3 as sq3
import numpy as np

from decimal import Decimal
from scipy import stats as scy

from src.config import Config
from src.utilities import Helper

from IPython import embed


if __name__ == '__main__':
    config = Config()
    sqlite = sq3.connect('/Users/alexmanelis/Development/Python/coinmarketcap-scraper/database.db')

    coins = [
        {'slug': 'bitcoin', 'symbol': 'btc'},
        {'slug': 'ethereum', 'symbol': 'eth'},
        {'slug': 'litecoin', 'symbol': 'ltc'},
        {'slug': 'monero', 'symbol': 'xmr'},

        {'slug': 'bitcoin-diamond', 'symbol': 'bcd'},
        {'slug': 'bitcoin-gold', 'symbol': 'bcg'},
        {'slug': 'dash', 'symbol': 'dash'},
        {'slug': 'marijuanacoin', 'symbol': 'mar'},
        {'slug': 'zcash', 'symbol': 'zec'},
    ]

    frame = {}
    stats = {}
    years = [2018, 2017, 2016, 2015, 2014, 2013]

    for year in years:
        config.logger.info(f'processing year {year}')

        frame[year] = {}
        stats[year] = {}

        for indx, coin in enumerate(coins):
            slug, symb = coin.get('slug', None), coin.get('symbol', None)

            if slug is None or symb is None:
                config.logger.info('skipping, found None type of [slug, symb]')
                continue

            rest = pd.read_sql_query(f'SELECT * FROM prices WHERE currency_slug = "{slug}" AND date(datetime) BETWEEN date("{year}-01-01") AND date("{year}-12-31") ORDER BY "datetime" DESC', sqlite)
            pusd = rest['price_usd']

            if pusd.empty:
                continue

            frame[year][symb] = pusd
            stats[year][symb] = {}

            stats[year][symb]['cov'] = '%.5E' % Decimal(np.cov(pusd).tolist())
            stats[year][symb]['var'] = '%.5E' % Decimal(np.var(pusd))
            stats[year][symb]['std'] = np.std(pusd)
            stats[year][symb]['mean'] = np.average(pusd)
            stats[year][symb]['median'] = np.median(pusd)
            stats[year][symb]['mode'] = scy.mode(pusd)[0][0]

        frame[year] = pd.DataFrame(frame[year])
        stats[year] = pd.DataFrame(stats[year])


    # frame = pd.DataFrame(frame)
    # stats = pd.DataFrame(stats)
    #
    # corr = frame.corr()





    #
    # fig = plt.figure()
    # plt.figure(figsize=(3,4))
    #
    # ax = fig.add_subplot(111)
    # cax = ax.matshow(corr, vmin=-1, vmax=1)
    # fig.colorbar(cax)
    # ticks = np.arange(0,9,1)
    # ax.set_xticks(ticks)
    # ax.set_yticks(ticks)
    # ax.set_xticklabels(list(data.columns.values))
    # ax.set_yticklabels(list(data.columns.values))
    # plt.show()

    #
    # print("Top Absolute Correlations")
    # print(Helper.get_top_abs_correlations(dframe, 30, True))
    # print(dframe.corr())
