from abc import ABCMeta, abstractmethod

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, Output, Input, dcc
from Analysis import AnalysisAge
from Base import BaseBlock


def report_player(df, app, mins=1000):
    sample_data = df[df['Min'] > mins]
    print(len(sample_data))
    report = Report(sample_data, app)
    player_info = PlayerInfo(sample_data, app)
    sidebar = html.Div(
        [
            player_info.render()
        ]
    )

    content = html.Div(
        [
            report.render()
        ]
    )
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(sidebar, width=3, className='bg-light'),
                    dbc.Col(content, width=9)
                ],
                style={"height": "90vh"}
            ),
        ],
        fluid=True
    )


def get_history(player_df):
    ret = [dbc.Row([dbc.Col('Year', width=3), dbc.Col('Team', width=4), dbc.Col('Salary', width=4)],
                   className='text-center')]
    for idx, row in player_df.iterrows():
        ret.append(dbc.Row([
            dbc.Col(row['year'], className='text-center', width=3),
            dbc.Col(row['Team'], className='text-center', width=4),
            dbc.Col('£' + format(int(row['Base Salary']), ',d'), className='text-end', width=4)
        ]))

    return ret


class PlayerInfo:
    def __init__(self, df, app):
        self.sample_data = df
        self._profile = Profile(self.sample_data, app)
        self._stats = PlayerStats(self.sample_data, app)

    def salary_top100(self):
        threshold = 100
        s_eda_df = self.sample_data.sort_values(by='Base Salary', ascending=False)
        return s_eda_df[~s_eda_df.duplicated(subset='Name', keep='first')].iloc[:threshold]['Name'].to_list()

    def render(self):
        return html.Div([
            dbc.Row([
                dbc.Select(
                    id="player-select",
                    options=[{'label': name, 'value': name} for name in self.salary_top100()],
                    value="Son Heung-Min"
                ),
            ]),

            dbc.Row(html.Div(id='player_profile')),
            dbc.Card(dbc.Row(
                dcc.Graph(
                    figure={},
                    id='player_stats',
                    config={
                        'displayModeBar': False
                    }
                )
            ))

        ])


class Profile(BaseBlock):
    def __init__(self, sample_data, app):
        super().__init__(app, 'Profile')
        self._sample_data = sample_data
        self._player_name = None
        self._player_df = None

    @property
    def player_df(self):
        return self._player_df

    def callbacks(self, app):
        @app.callback(
            Output("player_profile", "children"), [Input(component_id="player-select", component_property='value')]
        )
        def select_name(name):
            if name:
                self.change_player(name)
            return self.render()

    def change_player(self, player_name):
        self._player_name = player_name
        self._player_df = self._sample_data[self._sample_data['Name'] == player_name]

    def render(self):
        player_df = self._player_df.sort_values(by='year')
        return dbc.Card([dbc.Row([
            # image div
            dbc.Col(dbc.CardImg(
                src=f"https://d2zywfiolv4f83.cloudfront.net/img/players/{player_df['Player Id'].values[-1]}.jpg",
                top=True), width=4),

            # info div
            ## position, birth year, team
            dbc.Col(html.Div([
                html.H5(f'이름: {self._player_name}', className="card-title",
                        style={'margin-bottom': '10px', 'margin-top': '10px'}),
                html.Hr(),
                html.P(f"출생: {player_df['Birth Year'].values[-1]}({2023 - player_df['Birth Year'].values[-1]})",
                       className="card-text", ),
                html.P(f"포지션: {player_df['Position'].values[-1]}", className="card-text", ),
                html.P(f"소속: {player_df['Team'].values[-1]}", className="card-text", )
            ]), width=8, align='center')
        ]), dbc.Row([

            # history
            ## 연도 - 팀 - 연봉
            dbc.Col(html.Div([*get_history(player_df)]), width=12, className='text-end')
        ], style={'margin-top': '10px'})
        ], style={'height': '50vh'})


class PlayerStats(BaseBlock):
    def __init__(self, sample_data, app):
        super().__init__(app, 'PlayerStats')
        self._sample_data = sample_data
        self._player_name = None
        self._player_df = None

    def callbacks(self, app):
        @app.callback(
            Output(component_id="player_stats", component_property='figure'),
            [Input(component_id="player-select", component_property='value')]
        )
        def select_name(name):
            if name:
                self.change_player(name)
            return self.render()

    def change_player(self, player_name):
        self._player_name = player_name
        self._player_df = self._sample_data[self._sample_data['Name'] == player_name]

    def render(self):
        player_df = self._player_df.sort_values(by='year')
        position = player_df['Position'].values[-1]
        year_mean_df = self._sample_data[self._sample_data['Position'] == position].groupby('year')[
            'Base Salary'].mean().reset_index()
        fig = px.bar(
            year_mean_df,
            x='year',
            y='Base Salary',
            title='Salary',
            labels={'year': 'year', 'Base Salary': 'Salary'}
        )
        fig.add_scatter(x=player_df['year'], y=player_df['Base Salary'], mode='lines+markers', showlegend=False)
        fig.update_layout(title_text=f"Salary '{self._player_name}' vs Avg", title={'x': 0.5, 'y': 0.94}, margin_t=60,
                          margin_b=40, height=380)
        return fig


class Report:
    def __init__(self, sample_data, app):
        self._sample_data = sample_data
        self._app = app
        self._player_name = None
        self._analysis = AnalysisAge(self._sample_data, app)

    def __call__(self, *args, **kwargs):
        return self.render()

    def render(self):
        return html.Div([
            dbc.Row([dbc.Col(html.Div(id='player_age_analysis'))], style={'height': '32vh'}),
            dbc.Row([dbc.Col(html.Div(id='player_analysis2'))], style={'height': '32vh'}),
            dbc.Row([dbc.Col(html.Div(id='player_similar'))], style={'height': '31vh'})
        ])
