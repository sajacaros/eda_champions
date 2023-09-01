from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


def get_player():
    return pd.read_csv('../data/new/players_all.csv').drop('Unnamed: 0', axis=1)


def get_xbet():
    return (pd.read_csv('../data/new/1xbet_all.csv')
            .drop(['Team', 'Age', 'Position'], axis=1)
            .rename(columns={'Drb_x': 'Drb_Off', 'Drb_y': 'Drb_Def'}))


def get_understat():
    return (pd.read_csv('../data/new/understat_all.csv')
            .drop(['No', 'Team'], axis=1))


def get_capology():
    return pd.read_csv('../data/new/capology_all.csv')


def merge(player_df, xbet_df, understat_df, capology_df):
    # 프로필 + 연봉
    eda_df = player_df.merge(capology_df[['Weekly Salary', 'Base Salary', 'ADJ Salary', 'Name', 'year']], how='left',
                             left_on=['Name', 'year'], right_on=['Name', 'year'])
    eda_df = eda_df[~eda_df.duplicated(['year', 'Name'], keep='first')]  # 중복 제거
    # 프로필 + 연봉 + 스텟(understat)
    eda_df = eda_df.merge(understat_df, how='left', left_on=['Name', 'year'], right_on=['Name', 'year'])

    # 프로필 + 연봉 + 스텟(understat) + 스텟(1xbet)
    eda_df = eda_df.merge(
        xbet_df[[
            'Name', 'year', 'SpG', 'KeyP', 'Drb_Off', 'Fouled', 'Off',
            'Disp', 'UnsTch', 'Rating', 'Tackles', 'Inter', 'Fouls',
            'Offsides', 'Clear', 'Drb_Def', 'Blocks', 'AvgP', 'PS%']],
        how='left',
        left_on=['Name', 'year'],
        right_on=['Name', 'year']
    )
    return eda_df


def feature_check(eda_df):
    eda_df = eda_df.copy()
    eda_df = eda_df.dropna()
    eda_df.loc[:, 'Age Lev'] = eda_df['Age'].apply(
        lambda age:
        '<23' if age < 23 else
        '<25' if age < 25 else
        '<27' if age < 27 else
        '<30' if age < 30 else
        '<33' if age < 33 else
        '>33'
    )
    return eda_df


def get_data():
    # plyaer data load 및 정리(프로필)
    player_df = get_player()
    # 1xbet data load 및 정리(스텟)
    xbet_df = get_xbet()
    # understat data load 및 정리(스텟)
    understat_df = get_understat()
    # capology load(연봉)
    capology_df = get_capology()
    eda_df = merge(player_df, xbet_df, understat_df, capology_df)
    eda_df = feature_check(eda_df)
    return eda_df