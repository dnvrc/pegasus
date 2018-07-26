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
    def correlation_heatmap(self, df, title, absolute_bounds=True):
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

    @classmethod
    def get_redundant_pairs(self, df):
        pairs_to_drop = set()
        cols = df.columns
        for i in range(0, df.shape[1]):
            for j in range(0, i+1):
                pairs_to_drop.add((cols[i], cols[j]))

        return pairs_to_drop

    @classmethod
    def get_top_abs_correlations(self, df, n=5, a=False):
        au_corr = df.corr().abs().unstack()
        labels_to_drop = self.get_redundant_pairs(df)
        au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=a)
        au_corr.name = df.index.name

        return au_corr[0:n]
