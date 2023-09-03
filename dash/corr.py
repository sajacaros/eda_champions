import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, Output, Input


def corr_scatter(df, app):
    @app.callback(
        Output(component_id='controls-and-graph', component_property='figure'),
        Input(component_id='x-controls-and-radio-item', component_property='value'),
        Input(component_id='y-controls-and-radio-item', component_property='value'),
        Input(component_id='checklist', component_property='value'),
        Input(component_id='min', component_property='value')
    )
    def update_graph(x_col_chosen, y_col_chosen, positions, min):
        mask = df.Position.isin(positions)
        fig = px.scatter(
            df[(df['Min'] > min) & mask],
            x=x_col_chosen,
            y=y_col_chosen,
            color='Position',
            hover_name='Name',
            hover_data=['Team', 'Apps', 'Min', 'Position', 'year']
        )
        fig.update_layout(
            title_text=f"{x_col_chosen} Vs. {y_col_chosen}(출전시간 < {min}m)",
            title={'x': 0.5, 'y': 0.94},
            # margin_r=0,
            # margin_l=0,
            # height=300
        )
        return fig

    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                html.Div('Relationships between features with scatter', className="text-primary text-center fs-3")
            ]),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.Span('X축'), width=1),
                    dbc.Col(
                        dbc.RadioItems(
                            options=[{"label": x, "value": x} for x in df.columns],
                            value='Rating',
                            id='x-controls-and-radio-item',
                            inline=True
                        ),
                        width=11
                    )
                ]
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.Span('Y축'), width=1),
                    dbc.Col(
                        dbc.RadioItems(
                            options=[{"label": x, "value": x} for x in df.columns],
                            value='ADJ Salary',
                            id='y-controls-and-radio-item',
                            inline=True
                        ),
                        width=11
                    )
                ]
            ),
            dbc.Row([
                dbc.Row([
                    dbc.Col(html.Span('최저 출전 시간(m)'), width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            id="min",
                            options=[1000, 1100, 1200, 1300, 1400],
                            value=1000,
                            inline=True
                        ),
                        width=11
                    )
                ]),
                dbc.Row(dcc.Graph(figure={}, id='controls-and-graph',config={'displayModeBar': False})),
                dbc.Row([
                    dbc.Col(html.Span('포지션 선택'), width=1),
                    dbc.Col(
                        dcc.Checklist(
                            id="checklist",
                            options=["Forward", "Midfielder", "Defender", "Goalkeeper"],
                            value=["Forward", "Midfielder", "Defender", "Goalkeeper"],
                            inline=True
                        ),
                        width=11
                    )
                ])
            ])
        ])
    )