import datetime
import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from decimal import Decimal
from scipy import stats as scy

from src.models import Base
from src.utilities import Helper
from src.models.corr_0725.efficient_frontier import covmean_portfolio

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

        mean_returns = []
        main_coin_dt = {}

        total_frames = pd.DataFrame()

        for indx, coin in enumerate(self.model.entities):
            self.config.logger.info(f'Beginning processing for entity {coin}')

            slug, symb = coin.get('slug', None), coin.get('symbol', None)
            main_coin_dt[indx] = symb

            if slug is None or symb is None:
                self.config.logger.info('skipping, found None type of [slug, symb]')
                continue

            frm = pd.read_sql_query(f'SELECT * FROM prices WHERE currency_slug = "{slug}" AND date(datetime) BETWEEN date("{beg}-01-01") AND date("{end}-12-31") ORDER BY "datetime" DESC', self.connection)
            psd = frm['price_usd']

            if psd.empty:
                continue
            else:
                frame[symb] = psd

            # frm.to_excel(wr, sheet_name=symb) # print all data to seperate sheet with symbol as name

            mean_returns.append(np.average(psd.pct_change().dropna()))
            total_frames = total_frames.append(frm.dropna())

        # main_data_frame = pd.DataFrame(data=frame)
        # correlations = main_data_frame.corr()
        # covariances = main_data_frame.cov()
        #
        # weights, returns, risks, portfolios = covmean_portfolio(covariances, mean_returns)
        #
        # pd_weights = pd.DataFrame(data=weights)
        # pd_weights = pd_weights.rename(index=main_coin_dt, columns={0: 'Weights'})
        #
        # pd_returns = pd.DataFrame(data=returns)
        # pd_returns = pd_returns.rename(columns={0: 'Returns'})
        #
        # pd_risks = pd.DataFrame(data=risks)
        # pd_risks = pd_risks.rename(columns={0: 'Risks'})
        #
        # pd_portfolios = pd.DataFrame(data=portfolios)
        # pd_portfolios = pd_portfolios.rename(columns=main_coin_dt)
        #
        # pd_weights.to_excel(wr, sheet_name='Weights')
        # pd_returns.to_excel(wr, sheet_name='Returns')
        # pd_risks.to_excel(wr, sheet_name='Risks')
        # pd_portfolios.to_excel(wr, sheet_name='Portfolios')
        #
        # correlations.to_excel(wr, sheet_name='Correlations')
        # covariances.to_excel(wr, sheet_name='Covariances')

        # sns.lmplot(x='Risk', y='Return', data=pd_portfolios)
        # sns.boxplot(data=pd_risks)
        # sns.set_style('whitegrid')
        # sns.violinplot(x='Type 1', y='Attack', data=pd_portfolios)
        # plt.show()
        #
        # plt.style.use('seaborn')
        # plt.ylabel('Return')
        # plt.xlabel('Risk')
        # plt.plot(risks, returns, 'y-o')
        # plt.show()
        total_frames.to_excel(wr, sheet_name=f'Coins {beg}-{end}')
        wr.save()

        self.config.logger.info('Completed processing')
