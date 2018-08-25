import os
import re
import requests

from bs4 import BeautifulSoup
from IPython import embed


if __name__ == '__main__':
    # url = 'https://bitinfocharts.com/comparison/bitcoin-transactions.html'
    # url = 'https://bitinfocharts.com/comparison/monero-difficulty.html'
    url = 'https://bitinfocharts.com/comparison/difficulty-mining_profitability-xmr.html'
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
