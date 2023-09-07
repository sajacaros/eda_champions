import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, Output, Input
import plotly.figure_factory as ff

from report.Base import BaseBlock
from report.dictionary import stats_word


def numeric_analysis(df, app):
    return NumericAnalysis(df, app).render()


class NumericAnalysis(BaseBlock):
    def __init__(self,df,app):
        super().__init__(df, app, 'Numeric')
        self._numeric_columns = self._sample_data.select_dtypes('number').columns

    def callbacks(self, app):
        @app.callback(
            Output("box-graph", "figure"),
            [Input("select_column_num", "value"), Input("min-n", "value")]
        )
        def change_page_box(page, min):
            selected_column = self._numeric_columns[page]
            fig = px.box(
                self._sample_data[self._sample_data['Min'] > min],
                y=selected_column,
                hover_data=['Name', 'year', 'Position', 'Team'],
                color='Position'
            )
            fig.update_layout(
                title={
                    'text': f"{selected_column}{'('+stats_word[selected_column]+')' if selected_column in stats_word else ''}'s Box",
                    'y': 0.95,
                    'x': 0.5,
                    # 'xanchor': 'center',
                })
            return fig

        @app.callback(
            Output("kde-graph", "figure"),
            [Input("select_column_num", "value"), Input("min-n", "value")]
        )
        def change_page_kde(page, min_v):
            selected_column = self._numeric_columns[page]
            group_labels = ['distplot']  # name of the dataset
            fig = ff.create_distplot([self._sample_data.loc[self._sample_data['Min'] > min_v, selected_column].tolist()], group_labels, show_hist=False, show_rug=False)
            fig.update_layout(
                title={
                    'text': f"{selected_column}{'(' + stats_word[selected_column] + ')' if selected_column in stats_word else ''}'s Density Curve",
                    'y': 0.95,
                    'x': 0.5,
                },
                margin_t=60,
                showlegend=False
            )
            return fig


        @app.callback(
            Output("describe-text", "children"),
            [Input("select_column_num", "value"), Input("min-n", "value")],
        )
        def change_page_describe(page, min):
            selected_column = self._numeric_columns[page]
            s = self._sample_data.loc[self._sample_data['Min'] > min, selected_column].describe()
            return [dbc.Row([dbc.Col(column, className='text-center'), dbc.Col(round(v,2))]) for column, v in zip(s.index, s)]

    def render(self):
        return dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col([
                        dbc.RadioItems(
                            id="select_column_num",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": column_name, "value": idx} for idx, column_name in enumerate(self._numeric_columns)
                            ],
                            value=0,
                            style={'flex-wrap':'wrap'}
                        ),
                    ], width=2, className='bg-light border'),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(html.Span('최소 출전 시간'), width=1),
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
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure={}, id='kde-graph', config={'displayModeBar': False}), width=4),
                            dbc.Col(dcc.Graph(figure={}, id='box-graph', config={'displayModeBar': False}), width=5),
                            dbc.Col(html.Div(id='describe-text'), width=2, align='start', style={'margin-top': 50, 'display': 'block'}),
                        ],  align='center')
                    ], width=10)
                ])
            )
        )

