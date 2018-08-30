import os
import re
import requests

from bs4 import BeautifulSoup
from IPython import embed

methods = [
    {'key': 'transactions',             'comment': 'transactions',              'column': 'transactions'},
    {'key': 'size',                     'comment': 'block size',                'column': 'block_size'},
    {'key': 'confirmationtime',         'comment': 'block time',                'column': 'block_time'},
    {'key': 'difficulty',               'comment': 'difficulty',                'column': 'difficulty'},
    {'key': 'hashrate',                 'comment': 'hashrate',                  'column': 'network_hashrate'},
    {'key': 'price',                    'comment': 'price in USD',              'column': 'price_usd'},
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


if __name__ == '__main__':
    url = base_url('bitcoin', 'transactions')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    script_tag = soup.findAll('script')[5]
    script_text = script_tag.text

    pattern = re.compile(r'\[new Date\("\d{4}/\d{2}/\d{2}"\),\d*\w*\]')
    records = pattern.findall(script_text)

    embed()

    def parse_record(record):
        date = record[11:21]
        value = record[24:-1]
        return [date,value]


    for record in records:
        print(parse_record(record))
