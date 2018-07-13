import os
import numpy as np
import pandas as pd
import sqlite3 as sq3

from datetime import datetime

from src.api.generic import Generic
from src.api.quandl import QuandlAPI
from src.api.poloniex import PoloniexAPI
from src.utilities import Helper
from src.utilities import APPROVED_COLUMNS as AC

from src.config import Config

if __name__ == '__main__':
    config = Config()

    generic = Generic(config)
    qunadl = QuandlAPI(config)
    polonx = PoloniexAPI(config)

    exchange_data = qunadl.get_exchange_data()
    busd_datasets = Helper.merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'Weighted Price')

    Helper.clean_dataset(busd_datasets)
    Helper.append_average_column(busd_datasets, AC.btc_avg_usd)

    exchange_data = polonx.get_exchange_data(busd_datasets, AC.btc_avg_usd)
    pusd_datasets = Helper.merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), AC.price_usd)

    Helper.clean_dataset(pusd_datasets)

    pusd_datasets['BTC'] = busd_datasets[AC.btc_avg_usd]

    combined_df_2016 = pusd_datasets[pusd_datasets.index.year == 2016]
    combined_df_2016.pct_change().corr(method='pearson')
    print(combined_df_2016.tail())

    combined_df_2017 = pusd_datasets[pusd_datasets.index.year == 2017]
    combined_df_2017.pct_change().corr(method='pearson')
    print(combined_df_2017.tail())
