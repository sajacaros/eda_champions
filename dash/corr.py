import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Output, Input


def corr_scatter(df):

    @callback(
        Output(component_id='controls-and-graph', component_property='figure'),
        Input(component_id='x-controls-and-radio-item', component_property='value'),
        Input(component_id='y-controls-and-radio-item', component_property='value')
    )
    def update_graph(x_col_chosen, y_col_chosen):
        fig = px.scatter(
            df[df['Min'] > 1500],
            x=x_col_chosen,
            y=y_col_chosen,
            hover_name='Name',
            hover_data=["Team", "Apps", "Min", "Position", 'year']
        )
        return fig

    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div('Relationships between features with scatter', className="text-primary text-center fs-3")
            ]),
            html.Hr(),
            dbc.Row([
                dbc.RadioItems(
                    options=[{"label": x, "value": x} for x in df.columns],
                    value='Rating',
                    id='x-controls-and-radio-item',
                    inline=True
                )
            ]),
            html.Hr(),
            dbc.Row([
                dbc.RadioItems(
                    options=[{"label": x, "value": x} for x in df.columns],
                    value='ADJ Salary',
                    id='y-controls-and-radio-item',
                    inline=True
                )
            ]),

            dbc.Row([
                dcc.Graph(figure={}, id='controls-and-graph')
            ])
        ])
    )