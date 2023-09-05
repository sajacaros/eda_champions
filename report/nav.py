import dash_bootstrap_components as dbc

from corr import corr_scatter
from report_player import report_player
from report_team import report_team
from dictionary import explain_terms
from numeric_analysis import numeric_analysis


def tabs(df, app):
    return dbc.Tabs([
        dbc.Tab(corr_scatter(df, app), label='Correlation'),
        dbc.Tab(numeric_analysis(df, app), label='Numeric'),
        dbc.Tab(report_player(df, app), label='Report'),
        dbc.Tab(report_team(df, app), label='Team'),
        dbc.Tab(explain_terms(), label='Dictionary')
    ])
