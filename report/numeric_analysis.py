import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, Output, Input

from Base import BaseBlock


def numeric_analysis(df, app):
    return NumericAnalysis(df, app).render()


class NumericAnalysis(BaseBlock):
    def __init__(self,df,app):
        super().__init__(df, app, 'Numeric')
        self._numeric_columns = self._sample_data.select_dtypes('number').columns

    def callbacks(self, app):
        @app.callback(
            Output("selected-column", "children"),
            [Input("select_column_num", "active_page")],
        )
        def change_page_column(page):
            return self._numeric_columns[page-1 if page and page>0 else 0]


        @app.callback(
            Output("histogram-graph", "figure"),
            [Input("select_column_num", "active_page"), Input("min-n", "value")]
        )
        def change_page_kde(page, min):
            selected_column = self._numeric_columns[page-1 if page and page>0 else 0]
            return px.box(
                self._sample_data[self._sample_data['Min'] > min],
                y=selected_column,
                hover_data=['Name', 'year', 'Position']
            )

        @app.callback(
            Output("describe-text", "children"),
            [Input("select_column_num", "active_page")],
        )
        def change_page_describe(page):
            selected_column = self._numeric_columns[page-1 if page else 0]
            s = self._sample_data[selected_column].describe()
            return [dbc.Row([dbc.Col(column), dbc.Col(round(v,2))]) for column, v in zip(s.index, s)]

    def render(self):
        pagination = html.Div(
            dbc.Pagination(
                id='select_column_num',
                max_value=len(self._numeric_columns)
            ),
        )
        return dbc.Card(
            dbc.CardBody([
                dbc.Row([pagination], justify='center'),
                dbc.Row([
                    dbc.Col(html.Div(id='selected-column'),width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            id="min-n",
                            options=[0, *list(range(1000,2100,100))],
                            value=0,
                            inline=True,
                            inputStyle={"margin-right": "5px"},
                            labelStyle={"margin-right": "20px"}
                        ),
                        width=11
                    )]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.Div(id='describe-text'), width=2),
                    dbc.Col(dcc.Graph(figure={}, id='histogram-graph', config={'displayModeBar': False}), width=4),
                ], justify="evenly", align='center')
            ])
        )



