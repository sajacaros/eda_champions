import dash_bootstrap_components as dbc
from dash import Dash

from nav import tabs

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = tabs()

if __name__ == '__main__':
    app.run(debug=True)