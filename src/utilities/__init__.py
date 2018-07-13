import numpy as np
import pandas as pd

from dotmap import DotMap


APPROVED_COLUMNS = DotMap({
    'btc_avg_usd': 'AVG_BTC_USD',
    'price_usd': 'price_usd',
})


class Helper(object):
    @classmethod
    def append_average_column(self, dataset, column_name):
        dataset[column_name] = dataset.mean(axis=1)

    @classmethod
    def clean_dataset(self, dataset):
        dataset.replace(0, np.nan, inplace=True)

    @classmethod
    def merge_dfs_on_column(self, dataframes, labels, col):
        series_dict = {}

        for index in range(len(dataframes)):
            series_dict[labels[index]] = dataframes[index][col]

        return pd.DataFrame(series_dict)

    @classmethod
    def approved_column_names(self, name):
        return APPROVED_COLUMNS[name]

    @classmethod
    def correlation_heatmap(df, title, absolute_bounds=True):
        heatmap = go.Heatmap(
            z=df.corr(method='pearson').as_matrix(),
            x=df.columns,
            y=df.columns,
            colorbar=dict(title='Pearson Coefficient'),
        )

        layout = go.Layout(title=title)

        if absolute_bounds:
            heatmap['zmax'] = 1.0
            heatmap['zmin'] = -1.0

        fig = go.Figure(data=[heatmap], layout=layout)
        py.iplot(fig)
