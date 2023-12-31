import dash_bootstrap_components as dbc
from dash import html

from report.PlayerAnalysis import AnalysisAge, AnalysisStats
from report.PlyaerProfile import PlayerInfo
from report.Similarity import Similarity


def report_player(df, app, mins=1000):
    sample_data = df[df['Min'] > mins]
    report = ReportPlayer(sample_data, app)
    player_info = PlayerInfo(sample_data, app)
    sidebar = html.Div(
        [
            player_info.render()
        ]
    )

    content = html.Div(
        [
            report()
        ]
    )
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(sidebar, width=3, className='bg-light'),
                    dbc.Col(content, width=9)
                ],
                style={"height": "95vh"}
            ),
        ],
        fluid=True
    )


class ReportPlayer:
    def __init__(self, sample_data, app):
        self._age_analysis = AnalysisAge(sample_data, app)
        self._stats_analysis = AnalysisStats(sample_data, app)
        self._similarity_analysis = Similarity(sample_data, app)

    def __call__(self, *args, **kwargs):
        return self.render()

    def render(self):
        return html.Div([
            dbc.Row([dbc.Col(html.Div(id='player_stats_analysis'))]),
            dbc.Row([dbc.Col(html.Div(id='player_age_analysis'))]),
            dbc.Row([dbc.Col(html.Div(id='player_similarity'))])
        ])
