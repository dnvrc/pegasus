import datetime
import time
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
    years = [2018, 2017, 2016, 2015, 2014, 2013]

    # Data output
    ts = time.time()
    wr = pd.ExcelWriter('output-' + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx')

    for year in years:
        config.logger.info(f'Processing year {year}')

        frame[year] = {
            'frame': {},
            'stats': {},
        }

        for indx, coin in enumerate(coins):
            slug, symb = coin.get('slug', None), coin.get('symbol', None)

            if slug is None or symb is None:
                config.logger.info('skipping, found None type of [slug, symb]')
                continue

            frm = pd.read_sql_query(f'SELECT * FROM prices WHERE currency_slug = "{slug}" AND date(datetime) BETWEEN date("{year}-01-01") AND date("{year}-12-31") ORDER BY "datetime" DESC', sqlite)
            psd = frm['price_usd']

            if psd.empty:
                continue

            # Small bit of data cleansing
            frm = frm.drop(['id', 'price_btc', 'available_supply', 'currency_slug', 'volume_usd', 'market_cap_usd'], axis=1)

            frame[year]['frame'][symb] = psd #frm
            frame[year]['stats'][symb] = {}

            frame[year]['stats'][symb]['cov'] = '%.5E' % Decimal(np.cov(psd).tolist())
            frame[year]['stats'][symb]['var'] = '%.5E' % Decimal(np.var(psd))
            frame[year]['stats'][symb]['std'] = np.std(psd)
            frame[year]['stats'][symb]['mean'] = np.average(psd)
            frame[year]['stats'][symb]['median'] = np.median(psd)
            frame[year]['stats'][symb]['mode'] = scy.mode(psd)[0][0]


        frame[year]['stats'] = pd.DataFrame(frame[year]['stats'])
        frame[year]['stats'].index.name = f'{year} stats'

        frame[year]['frame'] = pd.DataFrame(frame[year]['frame'])
        frame[year]['frame'].index.name = f'{year} prices'

        # Data to Excel
        corr = frame[year]['frame'].corr()
        corr.index.name = f'{year} corr'

        stat = frame[year]['stats']
        main = frame[year]['frame']

        corr.to_excel(wr, sheet_name=f'{year}')
        stat.to_excel(wr, sheet_name=f'{year}', startrow=(len(coins) + 2))
        main.to_excel(wr, sheet_name=f'{year}', startrow=(len(coins) * 2) + 2)

    wr.save()


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
