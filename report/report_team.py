import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
import plotly.express as px

from report.Base import BaseBlock


def report_team(df, app, mins=1000):
    sample_data = df[df['Min'] > mins]
    report = ReportTeam(sample_data,app)

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(report()),
                ],
                style={"height": "90vh"}
            ),
        ],
        fluid=True
    )

def fig_update(fig, stats) :
    fig.update_layout(height=250, xaxis_title=None, title={'text': ' - '.join(stats), 'x': 0.5})


class ReportTeam(BaseBlock):
    stats_group = [['KeyP', 'SpG', 'Disp', 'Drb_Off'], ['G', 'xG', 'A', 'xA'], ['xGBuildup', 'xGChain']]

    def __init__(self, sample_data, app):
        super().__init__(sample_data, app)
        self._team_stats = self._sample_data.groupby('Team').mean(numeric_only=True).reset_index()

    def __call__(self, *args, **kwargs):
        return self.render()

    def callbacks(self, app):
        @app.callback(
            Output(component_id='team_graph-0', component_property='figure'),
            Input(component_id='team_checklist-0', component_property='value')
        )
        def update_graph(stats):
            fig = px.bar(self._team_stats, x='Team', y=stats, barmode='group')
            fig_update(fig, stats)
            return fig

        @app.callback(
            Output(component_id='team_graph-1', component_property='figure'),
            Input(component_id='team_checklist-1', component_property='value')
        )
        def update_graph(stats):
            fig = px.bar(self._team_stats, x='Team', y=stats, barmode='group')
            fig_update(fig, stats)
            return fig

        @app.callback(
            Output(component_id='team_graph-2', component_property='figure'),
            Input(component_id='team_checklist-2', component_property='value')
        )
        def update_graph(stats):
            fig = px.bar(self._team_stats, x='Team', y=stats, barmode='group')
            fig_update(fig, stats)
            return fig

    def render(self):
        return html.Div([
            self.team_stats_group()
        ])

    def team_stats_group(self):
        team_graph_group = []
        for n, stats in enumerate(ReportTeam.stats_group):
            team_graph_group.append(self.team_stats(stats, n))
        return dbc.Row(team_graph_group)

    def team_stats(self, stats, idx):
        return dbc.Row([
            dbc.Row([dbc.Col(html.Span(''), width=1),
                dbc.Col(
                    dcc.Checklist(
                        id=f"team_checklist-{idx}",
                        options=stats,
                        value=stats[0:2],
                        inline=True,
                        inputStyle={"margin-right": "5px"},
                        labelStyle={"margin-right": "20px"}
                    ),
                    width=11
                )
            ]),
            dbc.Row(dcc.Graph(figure={}, id=f'team_graph-{idx}', config={'displayModeBar': False})),
            html.Hr()
        ])
