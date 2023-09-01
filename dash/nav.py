import dash_bootstrap_components as dbc

from corr import corr_scatter
from report import report_player


def tabs(df, app):
    return dbc.Tabs([
        dbc.Tab(report_player(df, app), label='report'),
        dbc.Tab(corr_scatter(df, app), label='corr_scatter')
    ])
