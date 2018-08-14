import datetime
import time
import pandas as pd
import numpy as np

from decimal import Decimal
from scipy import stats as scy

from src.models import Base
from src.utilities import Helper


class Pipeline(Base):
    def __init__(self, config, connection, model):
        super(Pipeline, self).__init__(config, connection, model)

    def process(self):
        # Base frame to hold data
        frame = {}

        # Data output
        ts = time.time()
        wr = pd.ExcelWriter('output-' + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx')

        self.config.logger.info(f'Beginning processing for period {self.model.period}')

        for year in self.model.period:
            self.config.logger.info(f'Processing year {year}')

            frame[year] = {
                'frame': {},
                'stats': {},
            }

            for indx, coin in enumerate(self.model.entities):
                slug, symb = coin.get('slug', None), coin.get('symbol', None)

                if slug is None or symb is None:
                    self.config.logger.info('skipping, found None type of [slug, symb]')
                    continue

                frm = pd.read_sql_query(f'SELECT * FROM prices WHERE currency_slug = "{slug}" AND date(datetime) BETWEEN date("{year}-01-01") AND date("{year}-12-31") ORDER BY "datetime" DESC', self.connection)
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

            self.clean_print(corr)

            stat = frame[year]['stats']
            main = frame[year]['frame']
            slog = Helper.get_top_abs_correlations(corr, 30, True)

            stat_start = len(corr.index) + 2
            main_start = stat_start + len(stat.index) + 2
            slog_start = len(corr.columns) + 2

            corr.to_excel(wr, sheet_name=f'{year}')
            stat.to_excel(wr, sheet_name=f'{year}', startrow=stat_start)
            main.to_excel(wr, sheet_name=f'{year}', startrow=main_start)
            slog.to_excel(wr, sheet_name=f'{year}', startcol=slog_start)

        wr.save()
        self.config.logger.info('Completed processing')
