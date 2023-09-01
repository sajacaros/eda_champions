from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# plyaer data load 및 정리(프로필)
player_df = pd.read_csv('../data/new/players_all.csv')
player_df = player_df.rename(columns={'Unnamed: 0':'Id'}).drop(['No.', 'Id'], axis=1)
# 1xbet data load 및 정리(스텟)
xbet_df = pd.read_csv('../data/new/1xbet_all.csv')
xbet_df = xbet_df.drop(['Team','Age','Position'], axis=1).rename(columns={'Drb_x':'Drb_Off', 'Drb_y':'Drb_Def'})
# understat data load 및 정리(스텟)
understat_df = pd.read_csv('../data/new/understat_all.csv')
understat_df = understat_df.drop(['No','Team'], axis=1)
# capology load(연봉)
capology_df = pd.read_csv('../data/new/capology_all.csv')
# 프로필 + 연봉
eda_df = player_df.merge(capology_df[['Weekly Salary','Base Salary','ADJ Salary','Name', 'year']], how='left', left_on=['Name', 'year'], right_on=['Name', 'year'])
eda_df = eda_df[~eda_df.duplicated(['year', 'Name'], keep='first')] # 중복 제거
# 프로필 + 연봉 + 스텟(understat)
eda_df = eda_df.merge(understat_df, how='left', left_on=['Name', 'year'], right_on=['Name', 'year'])

# 프로필 + 연봉 + 스텟(understat) + 스텟(1xbet)
eda_df = eda_df.merge(
    xbet_df[[
        'Name', 'year', 'SpG', 'KeyP', 'Drb_Off', 'Fouled', 'Off',
        'Disp', 'UnsTch', 'Rating', 'Tackles', 'Inter','Fouls',
        'Offsides', 'Clear', 'Drb_Def', 'Blocks', 'AvgP', 'PS%']],
    how='left',
    left_on=['Name', 'year'],
    right_on=['Name', 'year']
)

eda_df = eda_df.dropna()
eda_df['Age Lev'] = eda_df['Age'].apply(lambda age: '<23' if age < 23 else '<25' if age <25 else '<27' if age<27 else '<30' if age<30 else '<33' if age<33 else '>33')

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('My First App with Data', className="text-primary text-center fs-3")
    ]),
    html.Hr(),
    dbc.Row([
        dbc.RadioItems(
            options=[{"label":x, "value":x} for x in eda_df.columns],
            value='Rating',
            id='x-controls-and-radio-item',
            inline=True
        )
    ]),
    html.Hr(),
    dbc.Row([
        dbc.RadioItems(
            options=[{"label":x, "value":x} for x in eda_df.columns],
            value='ADJ Salary',
            id='y-controls-and-radio-item',
            inline=True
        )
    ]),

    dbc.Row([
        dcc.Graph(figure={}, id='controls-and-graph')
    ])
])

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='x-controls-and-radio-item', component_property='value'),
    Input(component_id='y-controls-and-radio-item', component_property='value')
)
def update_graph(x_col_chosen,y_col_chosen):
    fig = px.scatter(eda_df, x=x_col_chosen, y=y_col_chosen)
    return fig

if __name__ == '__main__':
    app.run(debug=True)