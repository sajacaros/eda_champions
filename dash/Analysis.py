from dash import Output, Input, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from Base import BaseBlock
import engineering

feature_position = {
    'General': ['ADJ Salary', 'Apps', 'Min'],
    'Forward-o': ['G', 'xG', 'NPG', 'A', 'xA', 'Drb_Off'],
    'Forward-d': ['Tackles', 'Inter'],
    'Midfielder-o': ['G', 'xG', 'A', 'xA', 'xGBuildup', 'xGChain', 'KeyP', 'Drb_Off', 'AvgP', 'PS%'],
    'Midfielder-d': ['Tackles', 'Inter', 'Clear', 'Blocks'],
    'Defender-o': ['G', 'A', 'xGBuildup', 'AvgP', 'PS%'],
    'Defender-d': ['Tackles', 'Inter', 'Clear', 'Blocks', 'Drb_Def'],
    'Goalkeeper-o': ['xGBuildup', 'AvgP', 'PS%'],
    'Goalkeeper-d': ['Tackles', 'Inter', 'Clear', 'Blocks', 'Drb_Def']
}


class AnalysisAge(BaseBlock):
    def __init__(self, df, app):
        super().__init__(df, app, 'Analysis')

    def callbacks(self, app):
        @app.callback(
            Output(component_id="player_age_analysis", component_property='children'),
            [Input(component_id="player-select", component_property='value')]
        )
        def select_name(name):
            if name:
                self.change_player(name)
            return self.render()

        @app.callback(
            Output(component_id='age-offensive-graph', component_property='figure'),
            Input(component_id='age-offensive-radio-item', component_property='value')
        )
        def update_stats_offensive(y_col_chosen):
            return update_stats(y_col_chosen, 'Offensive')

        @app.callback(
            Output(component_id='age-defensive-graph', component_property='figure'),
            Input(component_id='age-defensive-radio-item', component_property='value')
        )
        def update_stats_defensive(y_col_chosen):
            return update_stats(y_col_chosen, 'Defensive')

        @app.callback(
            Output(component_id='age-general-graph', component_property='figure'),
            Input(component_id='age-general-radio-item', component_property='value')
        )
        def update_stats_general(y_col_chosen):
            return update_stats(y_col_chosen, 'General')

        def update_stats(y_col_chosen, category):
            position = self._player_df['Position'].to_list()[0]
            fig = px.line(labels={'x': 'Age', 'y': y_col_chosen})
            fig = fig.add_scatter(
                name='Avg',
                x=engineering.age_order,
                y=self._sample_data.groupby(['Position', 'Age Lev']).mean(numeric_only=True).loc[position, y_col_chosen],
                mode='lines+markers',
                showlegend=True
            )
            fig.add_scatter(
                name='Player',
                x=self._player_df['Age Lev'],
                y=self._player_df[y_col_chosen],
                mode='lines+markers',
                showlegend=True
            )
            fig.update_layout(
                title_text=f"{category} - '{y_col_chosen}' stats",
                title={'x': 0.5, 'y': 0.94},
                margin_r=0,
                margin_l=0,
                height=300,
                legend_yanchor="top",
                legend_y=0.99,
                legend_xanchor="left",
                legend_x=0.01,
                legend_bgcolor='rgba(0,0,0,0)'
            )
            return fig

    def render(self):
        return dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.RadioItems(
                        options=[{"label": x, "value": x} for x in
                                 feature_position[f"{self._player_df['Position'].to_list()[0]}-o"]],
                        value=feature_position[f"{self._player_df['Position'].to_list()[0]}-o"][0],
                        id='age-offensive-radio-item',
                        inline=True
                    )
                ]),
                dbc.Row([dcc.Graph(figure={}, id='age-offensive-graph', config={'displayModeBar': False})])
            ], width=4, align='end'),
            dbc.Col([
                dbc.Row([
                    dbc.RadioItems(
                        options=[{"label": x, "value": x} for x in
                                 feature_position[f"{self._player_df['Position'].to_list()[0]}-d"]],
                        value=feature_position[f"{self._player_df['Position'].to_list()[0]}-d"][0],
                        id='age-defensive-radio-item',
                        inline=True
                    )
                ]),
                dbc.Row([dcc.Graph(figure={}, id='age-defensive-graph', config={'displayModeBar': False})])
            ], width=4, align='end'),
            dbc.Col([
                dbc.Row([
                    dbc.RadioItems(
                        options=[{"label": x, "value": x} for x in
                                 feature_position['General']],
                        value=feature_position['General'][0],
                        id='age-general-radio-item',
                        inline=True
                    )
                ]),
                dbc.Row([dcc.Graph(figure={}, id='age-general-graph', config={'displayModeBar': False})])
            ], width=4, align='end'),
        ])

class AnalysisStats(BaseBlock):
    def __init__(self, df, app):
        super().__init__(df, app, 'Analysis')

    def callbacks(self, app):
        @app.callback(
            Output(component_id="player_stats_analysis", component_property='children'),
            [Input(component_id="player-select", component_property='value')]
        )
        def select_name(name):
            if name:
                self.change_player(name)
            return self.render()

        @app.callback(
            Output(component_id='g-graph', component_property='figure'),
            Input(component_id='player-select', component_property='value')
        )
        def update_stats_g(v):
            return update_stats(['xG', 'G'])

        @app.callback(
            Output(component_id='a-graph', component_property='figure'),
            Input(component_id='player-select', component_property='value')
        )
        def update_stats_a(v):
            return update_stats(['xA', 'A'])

        @app.callback(
            Output(component_id='xgbuildup-graph', component_property='figure'),
            Input(component_id='player-select', component_property='value')
        )
        def update_stats_xgbuildup(v):
            return update_stats(['xGBuildup'])

        @app.callback(
            Output(component_id='min-graph', component_property='figure'),
            Input(component_id='player-select', component_property='value')
        )
        def update_stats_min(v):
            return update_stats(['Min'])

        def update_stats(features: list):
            fig = px.line(labels={'x': 'year', 'y': f"{' - '.join(features)}"})
            fig = fig.add_scatter(
                name=features[0],
                x=self._player_df.year,
                y=self._player_df[features[0]],
                mode='lines+markers',
                showlegend=True
            )
            if len(features) > 1:
                fig.add_scatter(
                    name=features[1],
                    x=self._player_df.year,
                    y=self._player_df[features[1]],
                    mode='lines+markers'
                )

            fig.update_layout(
                title_text=f"{self._player_name}'s {' - '.join(features)}",
                title={'x': 0.5, 'y': 0.94},
                margin_r=0,
                margin_l=0,
                height=300,
                legend_yanchor="top",
                legend_y=0.99,
                legend_xanchor="left",
                legend_x=0.01,
                legend_bgcolor='rgba(0,0,0,0)'
            )
            # fig.update_xaxes(range=[2013, 2023])
            # self._sample_data
            return fig

    def render(self):
        return dbc.Row([
            dbc.Col([
                dbc.Row([dcc.Graph(figure={}, id='g-graph', config={'displayModeBar': False})])
            ], width=3, align='end'),
            dbc.Col([
                dbc.Row([dcc.Graph(figure={}, id='a-graph', config={'displayModeBar': False})])
            ], width=3, align='end'),
            dbc.Col([
                dbc.Row([dcc.Graph(figure={}, id='xgbuildup-graph', config={'displayModeBar': False})])
            ], width=3, align='end'),
            dbc.Col([
                dbc.Row([dcc.Graph(figure={}, id='min-graph', config={'displayModeBar': False})])
            ], width=3, align='end')
        ])