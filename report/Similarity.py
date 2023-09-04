import pandas as pd
from dash import Output, Input, html
from sklearn.preprocessing import RobustScaler
from sklearn.metrics.pairwise import cosine_similarity
from Base import BaseBlock
import dash_bootstrap_components as dbc


def create_profile(similarity_series):
    # image div
    return [
        dbc.Col([
            dbc.CardImg(
                src=f"https://d2zywfiolv4f83.cloudfront.net/img/players/{similarity_series['Player Id']}.jpg",
                top=True,
                # style={'height': 200, 'width': 150}
            ),
        ], width=1, align='center'),

        # info div
        ## position, birth year, team
        dbc.Col(
            html.Div([
                html.H5(f"이름: {similarity_series['Name']}", className="card-title",style={'margin-bottom': '10px', 'margin-top': '10px'}),
                html.Hr(),
                html.P(f"출생: {similarity_series['Birth Year']}({2023 - similarity_series['Birth Year']})", className="card-text"),
                html.P(f"포지션: {similarity_series['Position']}", className="card-text"),
                html.P(f"소속: {similarity_series['Team']}", className="card-text")
            ]), width=3
        )
    ]


def similarity_profile(similarity_df):
    p = []
    for idx in range(len(similarity_df)):
        p.extend(create_profile(similarity_df.iloc[idx]))
    return dbc.Row([
        dbc.Row([html.H5('--  유사도 분석  --', className='text-center')]),
        dbc.Row(p)
    ])


class CosineSimilarity(BaseBlock):
    def __init__(self, df, app):
        super(CosineSimilarity, self).__init__(df, app)
        self._scaled_df = self.scale(RobustScaler())

    def scale(self, scaler):
        featured_df = self._sample_data.copy()
        featured_df.Position = pd.factorize(featured_df.Position)[0]
        featured_df = featured_df.drop(
            [
                'Player Id', 'Name', 'Team', 'Birth Year', 'year',
                'Weekly Salary', 'Base Salary', 'ADJ Salary',
                'Age', 'Age Lev', 'Apps',
                'xG90', 'NPxG90', 'xA90', 'xGChain90', 'xGBuildup90',
                'xG90+xA90', 'NPxG90+xA90'
            ],
            axis=1
        )
        # ['Position', 'Min', 'G', 'NPG', 'A', 'xG', 'NPxG', 'xA','xGChain', 'xGBuildup', 'SpG',
        #  'KeyP', 'Drb_Off', 'Fouled', 'Off', 'Disp', 'UnsTch', 'Rating',
        #  'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear', 'Drb_Def', 'Blocks',
        #  'AvgP', 'PS%']
        return pd.DataFrame(
            scaler.fit_transform(featured_df),
            index=featured_df.index,
            columns=featured_df.columns
        )

    def callbacks(self, app):
        @app.callback(
            Output(component_id="player_similarity", component_property='children'),
            [Input(component_id="player-select", component_property='value')]
        )
        def select_name(name):
            if name:
                self.change_player(name)
            return self.render()

    def prepare_for_similarity(self):
        df = self._sample_data.copy()
        player_indexes = self._sample_data[self._sample_data['Name'] == self._player_name].index
        similarity = cosine_similarity(self._scaled_df.loc[list(player_indexes)], self._scaled_df)
        df['similarity'] = similarity.sum(axis=0)
        df['similarity-rank'] = df['similarity'].rank(ascending=False)
        return df[df['Name'] != self._player_name].sort_values('similarity-rank')

    def render(self):
        similarity_df = self.prepare_for_similarity()
        return similarity_profile(similarity_df[~similarity_df.duplicated(['Name'], keep='first')].iloc[:3])
