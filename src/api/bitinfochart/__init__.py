import os
import quandl
import re
import requests
import requests_cache

import numpy as np

from bs4 import BeautifulSoup as BS
from dateutil import parser
from decimal import Decimal

from src.db.models.currency import Currency
from src.db.models.share import Share
from src.db import database_session as session

from IPython import embed

currencies = [
    {'key': 'btc'},
    {'key': 'btg'},
    {'key': 'bch'},
    {'key': 'bcd'},
    {'key': 'etc'},
    {'key': 'eth'},
    {'key': 'etn'},
    {'key': 'eos'},
    {'key': 'ltc'},
    {'key': 'xrp'},
    {'key': 'neo'},
    {'key': 'trx'},
    {'key': 'omg'},
    {'key': 'dash'},
    {'key': 'doge'},
    {'key': 'xmr'},
    {'key': 'ada'},
    {'key': 'xlm'},
    {'key': 'zec'},
    {'key': 'iot'},
]

methods = [
    {'key': 'price',                    'comment': 'price in USD',              'column': 'price_usd'},
    {'key': 'transactions',             'comment': 'transactions',              'column': 'transactions'},
    {'key': 'size',                     'comment': 'block size',                'column': 'block_size'},
    {'key': 'confirmationtime',         'comment': 'block time',                'column': 'block_time'},
    {'key': 'difficulty',               'comment': 'difficulty',                'column': 'difficulty'},
    {'key': 'hashrate',                 'comment': 'hashrate',                  'column': 'network_hashrate'},
    {'key': 'sentbyaddress',            'comment': 'sent by address',           'column': 'sent_by_address'},
    {'key': 'sentinusd',                'comment': 'sent in USD',               'column': 'sent_in_usd'},
    {'key': 'mining_profitability',     'comment': 'mining profits',            'column': 'mining_profitability'},
    {'key': 'median_transaction_fee',   'comment': 'median transaction fee',    'column': 'median_transaction_fee'},
    {'key': 'mediantransactionvalue',   'comment': 'median transaction value',  'column': 'median_transaction_value'},
    {'key': 'marketcap',                'comment': 'protocol marketcap',        'column': 'marketcap'},
    {'key': 'transactionfees',          'comment': 'avg transaction fees',      'column': 'average_transaction_fee'},
    {'key': 'transactionvalue',         'comment': 'avg transaction value',     'column': 'average_transaction_value'},
    {'key': 'tweets',                   'comment': 'social / tweets per day',   'column': 'social_tweets'},
    {'key': 'activeaddresses',          'comment': 'active addresses',          'column': 'active_addresses'},
]


def base_url(coin_name, method_key) -> str:
    return f'https://bitinfocharts.com/comparison/{coin_name}-{method_key}.html'

def fetch_data(url) -> list:
    response = BS(requests.get(url).text, 'lxml')

    try:
        script_tag = response.findAll('script')[5]
    except:
        return None

    return re.compile(r'\[new Date\("\d{4}/\d{2}/\d{2}"\),\d*\.?\d*\w*\]').findall(script_tag.text)

def parse_record(record) -> dict:
    date = record[11:21]
    value = record[24:-1]
    return {'date': parser.parse(date).isoformat(), 'value': value}


if __name__ == '__main__':
    requests_cache.install_cache()

    quandl.ApiConfig.api_key = os.getenv('QUANDL_API_KEY', None)

    not_persisted = []

    for currency in currencies:
        symb = currency.get('key')
        symf = {}

        currency_model = session.query(Currency.Model).filter(Currency.Model.name == symb).first()

        if currency_model is None:
            continue

        print(f'Processing data for [{symb}] -> id[{currency_model.id}], slug[{currency_model.slug}]')

        hrate = None
        if symb == 'btc':
            hrate = quandl.get('BCHAIN/HRATE')

        for method in methods:
            m_key, m_cmt, m_clm = method.values()

            print(f' fetching data for {symb}[{m_key}]')
            rcd = fetch_data(base_url(symb, m_key))

            if rcd is None or not rcd:
                continue

            for r in rcd:
                d, v = parse_record(r).values()

                if 'null' in v:
                    v = None

                if d not in symf:
                    symf[d] = {}

                symf[d][m_clm] = v

        for date in list(symf.keys()):
            raw_entry = symf[date]
            share_mdl = Share.Model(**raw_entry)

            if share_mdl.network_hashrate == None or share_mdl.network_hashrate == '' or share_mdl.network_hashrate == 'null':
                date_index = date.split('T')[0]

                if hrate is not None and hrate.index.isin([date_index]).any():
                    share_mdl.network_hashrate = round(Decimal(hrate.loc[date_index].Value), 2)

            share_mdl.currency_id = currency_model.id
            share_mdl.currency_slug = currency_model.slug
            share_mdl.date = date

            not_persisted.append(share_mdl)

        #     session.add(share_mdl)
        # session.commit()

        session.bulk_save_objects(not_persisted)
        session.commit()
