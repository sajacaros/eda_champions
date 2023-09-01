import dash_bootstrap_components as dbc
from dash import Dash
import engineering

from nav import tabs


if __name__ == '__main__':
    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = tabs(engineering.get_data())

    app.run(debug=True)