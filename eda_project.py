import dash_bootstrap_components as dbc
from dash import Dash
from report import engineering
from report.nav import tabs

if __name__ == '__main__':
    external_stylesheets = [dbc.themes.FLATLY]  # CERULEAN]
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
    app.title = 'EDA 챔피언스⚽'
    app.layout = dbc.Container(tabs(engineering.get_data(parent_path='data'), app), fluid=True)

    app.run(debug=False)