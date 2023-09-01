import dash_bootstrap_components as dbc

from corr import corr_scatter
from report import report_player


def tabs():
    return dbc.Tabs([
        dbc.Tab(report_player(), label='report'),
        dbc.Tab(corr_scatter(), label='corr_scatter')
    ])
