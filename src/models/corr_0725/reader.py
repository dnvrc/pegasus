import datetime
import time
import pandas as pd
import numpy as np

from decimal import Decimal
from scipy import stats as scy

from src.models import Base
from src.utilities import Helper

from IPython import embed

class Reader(Base):
    def __init__(self, config, connection, model):
        super(Reader, self).__init__(config, connection, model)

    def process(self):
        # Base frame to hold data
        frame = {}

        # Data output
        ts = time.time()
        wr = pd.ExcelWriter('base-' + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx')

        self.config.logger.info(f'Beginning processing for period {self.model.period}')

        periods = sorted(self.model.period)
        beg, end = periods[0], periods[-1]

        for indx, coin in enumerate(self.model.entities):
            self.config.logger.info(f'Beginning processing for entity {coin}')

            slug, symb = coin.get('slug', None), coin.get('symbol', None)

            if slug is None or symb is None:
                self.config.logger.info('skipping, found None type of [slug, symb]')
                continue

            frm = pd.read_sql_query(f'SELECT * FROM prices WHERE currency_slug = "{slug}" AND date(datetime) BETWEEN date("{beg}-01-01") AND date("{end}-12-31") ORDER BY "datetime" DESC', self.connection)
            psd = frm['price_usd']

            if psd.empty:
                continue

            frm.to_excel(wr, sheet_name=symb)

        wr.save()
        self.config.logger.info('Completed processing')
