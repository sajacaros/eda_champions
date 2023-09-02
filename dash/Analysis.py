from dash import Output, Input, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from Base import BaseBlock
import engineering

feature_position = {
    'General': ['ADJ Salary', 'Apps', 'Min'],
    'Forward-o': ['G', 'xG', 'NPG', 'A', 'xA', 'Drb_Off'],
    'Forward-d': ['Tackles', 'Inter'],
    'Midfielder-o': ['G', 'xG', 'A', 'xA', 'xGBuildup', 'KeyP', 'Drb_Off', 'AvgP', 'PS%'],
    'Midfielder-d': ['Tackles', 'Inter', 'Clear', 'Blocks'],
    'Defender-o': ['G', 'xG', 'A', 'xA', 'xGBuildup', 'AvgP', 'PS%'],
    'Defender-d': ['Tackles', 'Inter', 'Clear', 'Blocks', 'Drb_Def'],
    'Goalkeeper-o': ['xGBuildup', 'AvgP', 'PS%'],
    'Goalkeeper-d': ['Tackles', 'Inter', 'Clear', 'Blocks', 'Drb_Def']
}


class AnalysisAge(BaseBlock):
    def __init__(self, df, app):
        super().__init__(app, 'Analysis')
        self._sample_data = df
        self._player_name = None
        self._player_df = None

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
            fig = px.line(
                x=engineering.age_order,
                y=self._sample_data.groupby(['Position', 'Age Lev']).mean(numeric_only=True).loc[
                    position, y_col_chosen],
                markers=True,
                labels={'x': 'Age', 'y': y_col_chosen}
            )
            fig.add_scatter(
                x=self._player_df['Age Lev'],
                y=self._player_df[y_col_chosen],
                mode='lines+markers',
                showlegend=False
            )
            fig.update_layout(
                title_text=f"{category} - '{y_col_chosen}' stats",
                title={'x': 0.5, 'y': 0.94},
                margin_r=0,
                margin_l=0,
                height=300
            )
            return fig

    def change_player(self, player_name):
        self._player_name = player_name
        self._player_df = self._sample_data[self._sample_data['Name'] == player_name]

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