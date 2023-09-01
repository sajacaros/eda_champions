from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

def report_player():
    return dbc.Card(
        dbc.CardBody([
            html.Div('report', className="text-primary text-center fs-3")
        ])
    )