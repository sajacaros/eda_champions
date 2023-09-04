import dash_bootstrap_components as dbc

from corr import corr_scatter
from report import report_player
from dictionary import explain_terms


def tabs(df, app):
    return dbc.Tabs([
        dbc.Tab(corr_scatter(df, app), label='correlation'),
        dbc.Tab(report_player(df, app), label='report'),
        dbc.Tab(explain_terms(), label='dictionary')
    ])
