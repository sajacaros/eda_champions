from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


def report_player(df):
    report = Report(df)
    return dbc.Card(
        dbc.CardBody([
            html.Div('report', className="text-primary text-center fs-3"),
            report()
        ])
    )


class Report:
    def __init__(self, eda_df):
        self._eda_df = eda_df

    def __call__(self, *args, **kwargs):
        return self.render()

    def render(self):
        @callback(
            Output("player_name", "children"), [Input(component_id="player-select", component_property='value')]
        )
        def select_name(name):
            if name:
                return name
            return 'Son Heung-Min'

        return html.Div([
            dbc.Select(
                id="player-select",
                options=[
                    {"label": "Eden Hazard", "value": "Eden Hazard"},
                    {"label": "Son Heung-Min", "value": "Son Heung-Min"},
                    {"label": "Cristiano Ronaldo", "value": "Cristiano Ronaldo"}
                ],
                value="Son Heung-Min"
            ),

            html.P(id='player_name'),
        ])
