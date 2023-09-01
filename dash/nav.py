import dash_bootstrap_components as dbc

from corr import corr_scatter
from report import report_player


def tabs(df):
    return dbc.Tabs([
        dbc.Tab(report_player(df), label='report'),
        dbc.Tab(corr_scatter(df), label='corr_scatter')
    ])
